from fatalis_project.fatalis_manager_main.asset_manager.asset_manager_ui import AssetManagerInterface, AssetManagerApplication
from fatalis_project.maya.asset_manager_maya import asset_manager_maya_utils


class AssetManagerApplicationMaya(AssetManagerApplication):
    """
    The AssetManagerApplicationMaya is the iteration of the AssetManagerInterface for Maya.
    """
    def fill_tabs(self):
        """
        create the tabs of widgets who would be shown in the AssetManagerInterface in Maya.
        """
        tabs = asset_manager_maya_utils.create_tab()
        for each_tab in tabs:
            self.asset_manager_layout.addWidget(each_tab[0])
            self.asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])


class AssetManagerInterfaceMaya(AssetManagerInterface):
    """
    The Maya AssetManagerInterfaceMaya is the iteration of the AssetManagerInterface for Maya.
    """
    INTERFACE_NAME = 'Asset Manager Interface Maya'
    APPLICATION = AssetManagerApplicationMaya
