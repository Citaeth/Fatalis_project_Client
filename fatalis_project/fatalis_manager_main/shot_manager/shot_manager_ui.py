from PySide6 import QtWidgets
import qfluentwidgets
from fatalis_project.fatalis_manager_main.shot_manager import shot_manager_utils


class ShotManagerApplication(QtWidgets.QWidget):
    """
    ShotManagerApplication build the layout/widgets contained in the ShotManagerInterface.
    """
    def __init__(self, parent=None):
        super(ShotManagerApplication, self).__init__(parent=None)

        self.asset_manager_layout = QtWidgets.QHBoxLayout(self)

        self.fill_tabs()

    def fill_tabs(self):
        """
        create the tabs of widgets who would be shown in the ShotManagerInterface.
        """
        tabs = shot_manager_utils.create_tab()
        for each_tab in tabs:
            self.asset_manager_layout.addWidget(each_tab[0])
            self.asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])


class ShotManagerInterface(qfluentwidgets.SingleDirectionScrollArea):
    """
    The Asset Manager Interface is a Widget who contain the Shot Manager.
    Should be called in the Fatalis Project main UI. It could be bypassed in the Shot Manager in the software, calling
    directly the ShotManagerApplication.
    """
    INTERFACE_NAME = 'Shot Manager Interface'
    APPLICATION = ShotManagerApplication
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.view = QtWidgets.QWidget(self)
        self.vBoxLayout = QtWidgets.QVBoxLayout(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName(self.INTERFACE_NAME)
        self.appShotManager = self.APPLICATION(self)
        self.vBoxLayout.addWidget(self.appShotManager)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 15, 0)

        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')