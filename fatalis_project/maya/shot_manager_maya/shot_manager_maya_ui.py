from fatalis_project.maya.shot_manager_maya import shot_manager_maya_utils
from fatalis_project.fatalis_manager_main.shot_manager import shot_manager_ui


class ShotManagerApplicationMaya(shot_manager_ui.ShotManagerApplication):
    """
    """
    def fill_tabs(self):
        tabs=shot_manager_maya_utils.create_tab()
        for each_tab in tabs:
            self.asset_manager_layout.addWidget(each_tab[0])
            self.asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])

class ShotManagerInterfaceMaya(shot_manager_ui.ShotManagerInterface):
    """
    The Asset Manager Interface is a Widget who contain the Shot Manager.
    Should be called in the Fatalis Project main UI. It could be bypassed in the Shot Manager in the software, calling
    directly the ShotManagerApplication.
    """
    INTERFACE_NAME = 'Shot Manager Interface Maya'
    APPLICATION = ShotManagerApplicationMaya


