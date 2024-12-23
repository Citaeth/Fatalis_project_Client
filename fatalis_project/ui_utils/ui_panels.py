import os
import glob
import re
from PySide6 import QtWidgets, QtCore, QtGui
import qfluentwidgets
from win32com.client import Dispatch
from functools import partial

from fatalis_project.ui_utils import utils

class TreePanel(QtWidgets.QFrame):
    """
    Base instance of the ThreePanel Widget, used to show the assets or shots list, to filter the main table content.
    This class should be overridden by subclasses depending on the software or if we are in asset or shot context.
    """
    def __init__(self, enable_check=False):
        super().__init__()
        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.tree = qfluentwidgets.TreeWidget(self)
        self.hBoxLayout.addWidget(self.tree)

        self.fill_tree()
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)

        if enable_check:
            it = QtWidgets.QTreeWidgetItemIterator(self.tree)
            while(it.value()):
                it.value().setCheckState(0, QtCore.Qt.Unchecked)
                it += 1

    def fill_tree(self):
        """
        Fill the tree depending on what we except in the context. This is the function that should be overridden.
        """
        pass

class TaskFilterPanel(QtWidgets.QWidget):
    """
    Base instance of the TaskFilterPanel Widget, used to show a list of the task of the project to filter elements
    in the main table.
    This class should be overridden by subclasses depending on the software or if we are in asset or shot context.
    """
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.listWidget = qfluentwidgets.ListWidget(self)

        stands = self.define_stand()
        for stand in stands:
            item = QtWidgets.QListWidgetItem(stand)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)

    def define_stand(self):
        """
        define the stands that we want to use to filter elements in the main tab UI depending on the context.
        This is the function that should be overridden.
        :return: list[str] Stands used to filter the tasks.
        """
        stands = [
            "Concept",
            "Modeling",
            "Texturing",
            "Lookdev",
            "Rigging",
            "Layout",
            "Animation",
            "Lighting",
            "Matte",
            "Compositing",
            "Editing",
        ]
        return stands

class FilterBarPanel(QtWidgets.QWidget):
    """
    Base instance of the FilterBarPanel Widget, used to let the artist filter what he wants in the main tab UI
    by taping in the filter bar.
    """
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.lineEdit = qfluentwidgets.SearchLineEdit(self)
        self.search_button = qfluentwidgets.PushButton('Search', self)

        stands = [
            "concept",
            "modeling",
            "texturing",
            "lookdev",
            "rigging",
            "layout",
            "animation",
            "lighting",
            "matte",
            "compositing",
            "editing",
        ]
        self.completer = QtWidgets.QCompleter(stands, self.lineEdit)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.lineEdit.setCompleter(self.completer)

        self.hBoxLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.lineEdit, 1)
        self.hBoxLayout.addWidget(self.search_button, 0, QtCore.Qt.AlignCenter)

        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Search stand')
        self.lineEdit.returnPressed.connect(self.search_button.click)


class MainTablePanel(QtWidgets.QWidget):
    """
    Base instance of the MainTablePanel Widget, used to show the list of assets, dpeending on the filters of the user.
    This class could be overridden by subclasses depending on the software or if we are in asset or shot context if
    needed.
    """
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.tableView = qfluentwidgets.TableWidget(self)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.tableView.setSortingEnabled(True)

        self.tableView.setBorderVisible(True)

        self.define_table_content()
        self.hBoxLayout.addWidget(self.tableView)

        self.tableView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.open_context_menu)

    def define_table_content(self):
        """
        define the row/column information, as name and width in the table.
        :return:
        """
        self.tableView.setRowCount(60)
        self.tableView.setColumnCount(9)
        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(['Asset Name',
                                                  '.ext',
                                                  'Task',
                                                  'Version',
                                                  'Owner',
                                                  'Date',
                                                  'Infos',
                                                  'asset_id',
                                                  'status'])

        self.tableView.setColumnWidth(0, 200)
        self.tableView.setColumnWidth(1, 65)
        self.tableView.setColumnWidth(2, 100)
        self.tableView.setColumnWidth(3, 80)
        self.tableView.setColumnWidth(4, 100)
        self.tableView.setColumnWidth(5, 150)
        self.tableView.setColumnWidth(6, 100)
        self.tableView.setColumnHidden(6, True)
        self.tableView.setColumnWidth(7, 10)
        self.tableView.setColumnHidden(7, True)
        self.tableView.setColumnWidth(8, 50)

    def update_table_with_asset_database(self, database_assets_infos):
        """
        fill the table with the datas of the assets, from the database information. Should be override depending
        on the context (asset or shot.)
        :param database_assets_infos: dictionnary who contain the assets database information.
        """
        pass

    def open_context_menu(self, position):
        """
        open a menu when right click in a row table.
        Use to refresh the content of the table, or to change the status of the selected asset version.
        :param position:
        """
        index = self.tableView.indexAt(position)
        if not index.isValid():
            return

        row = index.row()
        row_data = [self.tableView.item(row, col).text() for col in range(self.tableView.columnCount())]

        menu = qfluentwidgets.RoundMenu(self)
        action_refresh = QtGui.QAction("Refresh Table", self)
        action_refresh.setIcon(qfluentwidgets.FluentIcon.SYNC.icon())
        action_refresh.triggered.connect(self.refresh_table)
        menu.addAction(action_refresh)
        menu.addSeparator()
        config = utils.get_user_config_file()[0]
        status_name_list = config.find('./assets/status').text.split(", ")
        submenu = qfluentwidgets.RoundMenu("Change Status", self)
        submenu.setIcon(qfluentwidgets.FluentIcon.CHEVRON_RIGHT)
        for each_status in status_name_list:
            action = QtGui.QAction(each_status, self)
            action.triggered.connect(partial(self.change_status, row_data[7], each_status))
            submenu.addAction(action)
        menu.addMenu(submenu)
        menu.exec(self.tableView.mapToGlobal(position), aniType=qfluentwidgets.MenuAnimationType.DROP_DOWN)

    def refresh_table(self):
        """
        function to refresh the table, should be overridden to use the database needed, depending on assets or shot
        context.
        """
        print('coucou')
        pass

    def change_status(self, asset_id, status):
        """
        function to change the status of selected version.
        :param int asset_id: ID of the asset that should change its status. Need to send the information to server.
        :param str status: new status of the asset version.
        """
        pass


class InfoPanel(QtWidgets.QWidget):
    """
    Base instance of the InfoPanel Widget, used to show details of the version selected by the user in the MainTablePanel.
    This class could be overridden by subclasses depending on the software or if we are in asset or shot context if
    needed.
    """
    def __init__(self):
        super().__init__()
        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setStretch(0, 1)

        self.tableView = qfluentwidgets.TextEdit(self)
        self.tableView.setReadOnly(True)
        complex_text = """Coucou ceci est un espace info

                Il y aura beaucoup de choses et elements dedans

                - Petit element 1
                - Petit element 2

                et pleeeeins d'autres ensuite."""

        self.tableView.setPlainText(complex_text)
        self.hBoxLayout.addWidget(self.tableView)


class LoadingPanel(QtWidgets.QWidget):
    """
    Base instance of the LoadingPanel Widget, used to add buttons to deal with the elements on the server, for exemple
    to download file/folder, open the selected asset in maya, houdini, or open a Publisher UI.
    This class should be overridden by subclasses depending on the software or if we are in asset or shot context if
    needed.
    """
    def __init__(self, table_widget):
        super().__init__(table_widget)
        self.table_widget = table_widget
        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.create_buttons()

    def create_buttons(self):
        """
        create the buttons and add it to the LoadingPanel Widget.
        """
        pass

    def get_maya_path(self, user_config_root, user_config_tree, user_config_path):
        """
        Try to get automatically the maya.exe path, using the most common usage. If it's not found, open a dialog window
        to let the user point on the .exe, or a Link app, to get the .exe path.
        It will be added to the user_config, and used to open maya.
        :param user_config_root: the config root instance, used to read the data from the config.
        :param user_config_tree: the config tree instance, used to write the changes.
        :param user_config_path: the file config hard path, used to save it after writing using config_tree.
        :return:
        """
        versions=['2025', '2024']
        path_found = None
        for each_version in versions:
            default_path=r'C:\Program Files\Autodesk\Maya{}\bin\maya.exe'.format(each_version)
            if os.path.exists(default_path):
                path_found = True
                maya_app = default_path
                maya_version = each_version
                break
        if not path_found:
            get_maya_path = QtWidgets.QFileDialog()
            get_maya_path.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            if get_maya_path.exec_():
                maya_path = get_maya_path.selectedFiles()[0]
                if '.lnk' in maya_path:
                    shell = Dispatch("WScript.Shell")
                    maya_app = shell.CreateShortcut(maya_path).TargetPath
                else:
                    maya_app = maya_path
                    maya_version = re.search(r"Maya(\d{4})", maya_app).group(1)

        config_maya_path = user_config_root.find('./software/maya/path')
        config_maya_version = user_config_root.find('./software/maya/version')
        config_maya_path.text = maya_app
        config_maya_version.text = maya_version
        user_config_tree.write(user_config_path, encoding="utf-8", xml_declaration=True)
        return maya_app

    def get_houdini_path(self, user_config_root, user_config_tree, user_config_path):
        """
        Try to get automatically the houdini.exe path, using the most common usage. If it's not found, or if more than
        one version of houdini are found, open a dialog window to let the user point on the .exe, or a Link app,
        to get the .exe path.
        It will be added to the user_config, and used to open houdini.
        :param user_config_root: the config path root instance, used to read the data from the config.
        :param user_config_tree: the config tree instance, used to write the changes.
        :param user_config_path: the file config hard path, used to save it after writing using config_tree.
        :return:
        """
        houdini_paths = []
        base_path = r"C:\Program Files\Side Effects Software"
        search_pattern = os.path.join(base_path, "Houdini *", "bin", "houdini.exe")
        for houdini_path in glob.glob(search_pattern):
            houdini_paths.append(houdini_path)
        if houdini_paths and len(houdini_paths)==1:
            houdini_app = houdini_paths[0]
            houdini_version = re.search(r"Houdini (\d+\.\d+\.\d+)", houdini_app).group(1)
        else:
            get_houdin_path = QtWidgets.QFileDialog()
            get_houdin_path.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            if get_houdin_path.exec_():
                houdini_path = get_houdin_path.selectedFiles()[0]
                if '.lnk' in houdini_path:
                    shell = Dispatch("WScript.Shell")
                    houdini_app = shell.CreateShortcut(houdini_path).TargetPath
                else:
                    houdini_app = houdini_path
                    houdini_version = re.match(r"Houdini (\d+\.\d+\.\d+)", houdini_path)

        config_houdini_path = user_config_root.find('./software/houdini/path')
        config_houdini_version = user_config_root.find('./software/houdini/version')
        config_houdini_path.text = houdini_app
        config_houdini_version.text = houdini_version
        user_config_tree.write(user_config_path, encoding="utf-8", xml_declaration=True)
        return houdini_app
