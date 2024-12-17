import os
from PySide6 import QtWidgets, QtGui
import qfluentwidgets
from fatalis_project.ui_utils import utils
from fatalis_project.ui_utils.http_request.exporter_main import upload_to_server


class PublishWindow(qfluentwidgets.FluentWindow):
    """
    Window to publish file or folder on the server by the user.
    """
    INTERFACE_INSTANCE = None
    def __init__(self):
        super(PublishWindow, self).__init__()
        self.setWindowTitle('Publisher')
        self.setWindowIcon(QtGui.QIcon(':/qfluentwidgets/images/icons/Share_white.svg'))
        qfluentwidgets.setTheme(qfluentwidgets.Theme.DARK)
        qfluentwidgets.setThemeColor("#8e3838", save=False)
        self.resize(650, 350)

        self.add_navigations_interface()

    def add_navigations_interface(self):
        """
        add the interface tabs to the FluentWindow. It creates one tabs at the right for each new subInterface.
        In the case of the Publisher one, we want to hide the tab, as there is only one.
        :return:
        """
        self.publisher_interface = PublisherInterface(self)
        self.addSubInterface(self.publisher_interface, text='Publisher', icon=qfluentwidgets.FluentIcon.SHARE)
        self.navigationInterface.hide()


class PublisherApplication(QtWidgets.QWidget):
    """
    PublisherApplication build the layout/widgets contained in the PublisherInterface.
    """
    CONFIG = utils.get_user_config_file()[0]
    def __init__(self, parent=None):
        super(PublisherApplication, self).__init__(parent)
        self.asset_manager_layout = QtWidgets.QVBoxLayout(self)

        self.build_name_task_tab()
        self.build_path_tab()
        self.build_info_publish_tab()

    def build_name_task_tab(self):

        asset_name_list = self.CONFIG.find('./assets/name').text.split(", ")
        asset_task_list = self.CONFIG.find('./assets/task').text.split(", ")
        status_list = self.CONFIG.find('./assets/status').text.split(", ")
        name_task_widget = QtWidgets.QWidget()
        name_task_layout = QtWidgets.QHBoxLayout()
        name_task_widget.setLayout(name_task_layout)
        self.name_version_widget = QtWidgets.QLineEdit('Enter Version Name')
        name_version_layout = QtWidgets.QHBoxLayout(self.name_version_widget)

        self.asset_name_widget = QtWidgets.QComboBox()
        self.asset_name_widget.addItems(asset_name_list)
        name_version_layout = QtWidgets.QVBoxLayout(self.asset_name_widget)
        self.asset_task_widget = QtWidgets.QComboBox()
        self.asset_task_widget.addItems(asset_task_list)
        asset_task_layout = QtWidgets.QHBoxLayout(self.asset_task_widget)

        name_task_layout.addWidget(self.name_version_widget)
        name_task_layout.addWidget(self.asset_name_widget)
        name_task_layout.addWidget(self.asset_task_widget)
        self.asset_manager_layout.addWidget(name_task_widget)

    def build_path_tab(self):

        path_widget = QtWidgets.QWidget()
        path_layout = QtWidgets.QHBoxLayout(path_widget)
        path_button = QtWidgets.QPushButton('Give a Path:')
        path_button.clicked.connect(self.get_path)
        self.path_search = QtWidgets.QLineEdit()
        self.path_search.setReadOnly(True)

        path_layout.addWidget(path_button)
        path_layout.addWidget(self.path_search)
        self.asset_manager_layout.addWidget(path_widget)

    def build_info_publish_tab(self):

        info_publish_widget = QtWidgets.QWidget()
        info_publish_layout = QtWidgets.QHBoxLayout(info_publish_widget)

        self.info_widget = qfluentwidgets.TextEdit()
        self.info_widget.setPlainText('Gives some infos if necessary')
        info_layout = QtWidgets.QHBoxLayout(self.info_widget)

        publish_button = qfluentwidgets.PushButton('Publish')
        publish_button.clicked.connect(self.publish_assets)

        info_publish_layout.addWidget(self.info_widget)
        info_publish_layout.addWidget(publish_button)
        self.asset_manager_layout.addWidget(info_publish_widget)

    def get_path(self):
        path = QtWidgets.QFileDialog()
        path.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if path.exec_():
            self.fileNames = path.selectedFiles()
            self.fileNames = self.fileNames[0] if len(self.fileNames) == 1 else self.fileNames
            fileNames_text = str(self.fileNames) if isinstance(self.fileNames, list) else self.fileNames
            self.path_search.setText(fileNames_text)

    def publish_assets(self):

        asset_version_name = self.name_version_widget.text()
        if asset_version_name == '' or asset_version_name == 'Enter Version Name':
            self.publish_missing_infos_dialog('it missing the version name information to do the Publish!')
            return
        asset_name = self.asset_name_widget.currentText()
        if not asset_name.lower() in asset_version_name.lower():
            self.publish_missing_infos_dialog('the version name should contain the asset name please!')
            return
        asset_task = self.asset_task_widget.currentText()
        user_name = self.CONFIG.find('./user/name').text
        infos = self.info_widget.toPlainText()
        infos = '' if infos == 'Gives some infos if necessary' else infos
        path = self.fileNames
        if isinstance(path, list):
            zip_file = utils.convert_files_group_to_zip(path)
            upload_to_server(zip_file, asset_version_name, asset_name, asset_task, user_name, infos)
            os.remove(zip_file)
        else:
            upload_to_server(path, asset_version_name, asset_name, asset_task, user_name, infos)

    def publish_missing_infos_dialog(self, message):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle('Publish issue, missing information')
        dlg.setText(message)
        button = dlg.exec()

        if button == QtWidgets.QMessageBox.Ok:
            print('OK!')


class PublisherInterface(qfluentwidgets.SingleDirectionScrollArea):
    """
    create the interface for the publisher widgets.
    """
    INTERFACE_NAME = 'PublisherInterface'
    APPLICATION=PublisherApplication
    def __init__(self, parent=None):
        super(PublisherInterface, self).__init__(parent)

        self.view = QtWidgets.QWidget(self)
        self.vBoxLayout = QtWidgets.QVBoxLayout(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName(self.INTERFACE_NAME)
        self.appPublisher = self.APPLICATION(self)
        self.vBoxLayout.addWidget(self.appPublisher)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)

        self.setStyleSheet('QScrollArea {border: none; background:transparent}')
        self.view.setStyleSheet('QWidget {background:transparent}')


def open_publisher():
    if PublishWindow.INTERFACE_INSTANCE:
        PublishWindow.INTERFACE_INSTANCE.close()
        PublishWindow.INTERFACE_INSTANCE = None
    PublishWindow.INTERFACE_INSTANCE = PublishWindow()
    PublishWindow.INTERFACE_INSTANCE.show()
