from PySide6 import QtWidgets
import qfluentwidgets
from fatalis_project.fatalis_manager_main.asset_manager import asset_manager_utils


class AssetManagerApplication(QtWidgets.QWidget):
    """
    AssetManagerApplication build the layout/widgets contained in the AssetManagerInterface.
    """
    def __init__(self, parent):
        super(AssetManagerApplication, self).__init__(parent)

        self.asset_manager_layout = QtWidgets.QHBoxLayout(self)
        self.fill_tabs()

    def fill_tabs(self):
        """
        create the tabs of widgets who would be shown in the AssetManagerInterface.
        """
        assets_data_base_infos = self.parent().parent().asset_data_base
        tabs = asset_manager_utils.create_tab(assets_data_base_infos)
        for each_tab in tabs:
            self.asset_manager_layout.addWidget(each_tab[0])
            self.asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])


class AssetManagerInterface(qfluentwidgets.SingleDirectionScrollArea):
    """
    The Asset Manager Interface is a Widget who contain the Asset Manager.
    Should be called in the Fatalis Project main UI. It could be bypassed in the Asset Manager in the software, calling
    directly the AssetManagerApplication.
    """
    INTERFACE_NAME = 'Asset Manager Interface'
    APPLICATION = AssetManagerApplication
    def __init__(self, parent):
        super().__init__(parent)
        self.view = QtWidgets.QWidget(self)
        self.vBoxLayout = QtWidgets.QVBoxLayout(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName(self.INTERFACE_NAME)
        self.appAssetManager = self.APPLICATION(self)
        self.vBoxLayout.addWidget(self.appAssetManager)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 15, 0)

        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')

