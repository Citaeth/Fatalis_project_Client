from fatalis_project.maya.shot_manager_maya import shot_manager_maya_utils
from fatalis_project.fatalis_manager_main.shot_manager import shot_manager_ui


class ShotManagerApplicationMaya(shot_manager_ui.ShotManagerApplication):
    """
    The ShotManagerApplicationMaya is the iteration of the AssetManagerInterface for Maya.
    """
    def fill_tabs(self):
        """
        create the tabs of widgets who would be shown in the ShotManagerInterface in Maya.
        """
        tabs=shot_manager_maya_utils.create_tab()
        for each_tab in tabs:
            self.asset_manager_layout.addWidget(each_tab[0])
            self.asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])

class ShotManagerInterfaceMaya(shot_manager_ui.ShotManagerInterface):
    """
    The ShotManagerInterfaceMaya is the iteration of the AssetManagerInterface for Maya.
    """
    INTERFACE_NAME = 'Shot Manager Interface Maya'
    APPLICATION = ShotManagerApplicationMaya


