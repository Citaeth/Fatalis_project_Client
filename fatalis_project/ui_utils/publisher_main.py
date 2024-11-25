from PySide6 import QtWidgets, QtGui
import qfluentwidgets


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
        self.resize(500, 350)

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
    def __init__(self, parent=None):
        super(PublisherApplication, self).__init__(parent)


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
