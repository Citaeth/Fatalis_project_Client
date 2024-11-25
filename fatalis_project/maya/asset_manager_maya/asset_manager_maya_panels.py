import qfluentwidgets
from fatalis_project.fatalis_manager_main.asset_manager import asset_manager_panels


class MayaAssetTreePanel(asset_manager_panels.AssetTreePanel):
    """
    Maya iteration for the AssetTreePanel, override if needed change in maya from the main in asset manager panels.
    """


class MayaAssetTaskFilterPanel(asset_manager_panels.AssetTaskFilterPanel):
    """
    Maya iteration for the AssetTaskFilterPanel, override if needed change in maya from the main in asset manager panels.
    """


class MayaAssetFilterBarPanel(asset_manager_panels.AssetFilterBarPanel):
    """
    Maya iteration for the AssetFilterBarPanel, override if needed change in maya from the main in asset manager panels.
    """


class MayaAssetMainTablePanel(asset_manager_panels.AssetMainTablePanel):
    """
    Maya iteration for the AssetMainTablePanel, override if needed change in maya from the main in asset manager panels.
    """


class MayaAssetInfoPanel(asset_manager_panels.AssetInfoPanel):
    """
    Maya iteration for the AssetInfoPanel, override if needed change in maya from the main in asset manager panels.
    """


class MayaAssetLoadingPanel(asset_manager_panels.AssetLoadingPanel):
    """
    Maya iteration for the AssetLoadingPanel, override if needed change in maya from the main in asset manager panels.
    """

    def create_buttons(self):
        load_in_maya_button = qfluentwidgets.PushButton('Load Asset in Maya')
        load_in_maya_button.clicked.connect(self.load_asset_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

    def load_asset_in_maya(self):
        print('Loading Asset in Maya')
