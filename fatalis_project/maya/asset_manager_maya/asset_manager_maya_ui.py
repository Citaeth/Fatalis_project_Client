from fatalis_project.fatalis_manager_main.asset_manager.asset_manager_ui import AssetManagerInterface, AssetManagerApplication
from fatalis_project.maya.asset_manager_maya import asset_manager_maya_utils


class AssetManagerApplicationMaya(AssetManagerApplication):
    """
    """
    def fill_tabs(self):
        tabs = asset_manager_maya_utils.create_tab()
        for each_tab in tabs:
            self.asset_manager_layout.addWidget(each_tab[0])
            self.asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])


class AssetManagerInterfaceMaya(AssetManagerInterface):
    """
    The Asset Manager Interface is a Widget who contain the Asset Manager.
    Should be called in the Fatalis Project main UI. It could be bypassed in the Asset Manager in the software, calling
    directly the AssetManagerApplication.
    """
    INTERFACE_NAME = 'Asset Manager Interface Maya'
    APPLICATION = AssetManagerApplicationMaya
