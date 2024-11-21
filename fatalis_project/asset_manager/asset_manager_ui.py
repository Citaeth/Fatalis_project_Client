from PySide6 import QtWidgets

from fatalis_project.ui_utils import ui_utils as utils
from fatalis_project.asset_manager import asset_manager_utils


class AssetManagerInterface(utils.SingleDirectionScrollInterface):
    """
    The Asset Manager Interface is a Widget who contain the Asset Manager.
    Should be called in the Fatalis Project main UI. It could be bypassed in the Asset Manager in the software, calling
    directly the AssetManagerApplication.
    """
    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.setObjectName('Asset Manager Interface')
        self.appAssetManager = AssetManagerApplication(self)
        self.vBoxLayout.addWidget(self.appAssetManager)


class AssetManagerApplication(QtWidgets.QWidget):
    """

    """
    def __init__(self, parent=None):
        super(AssetManagerApplication, self).__init__(parent=None)

        asset_manager_layout = QtWidgets.QHBoxLayout()
        self.setLayout(asset_manager_layout)

        tabs=asset_manager_utils.create_tab()
        for each_tab in tabs:
            asset_manager_layout.addWidget(each_tab[0])
            asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])
