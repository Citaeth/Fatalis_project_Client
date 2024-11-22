from PySide6 import QtWidgets

from fatalis_project.maya.shot_manager_maya import shot_manager_maya_utils
from fatalis_project.shot_manager import shot_manager_ui


class ShotManagerInterfaceMaya(shot_manager_ui.ShotManagerInterface):
    """
    The Asset Manager Interface is a Widget who contain the Shot Manager.
    Should be called in the Fatalis Project main UI. It could be bypassed in the Shot Manager in the software, calling
    directly the ShotManagerApplication.
    """
    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.setObjectName('Shot Manager Interface Maya')
        self.appShotManager = ShotManagerApplicationMaya(self)
        self.vBoxLayout.addWidget(self.appShotManager)

class ShotManagerApplicationMaya(shot_manager_ui.ShotManagerApplication):
    """

    """
    def __init__(self, parent=None):
        super(ShotManagerApplicationMaya, self).__init__(parent=None)

        asset_manager_layout = QtWidgets.QHBoxLayout()
        self.setLayout(asset_manager_layout)

        tabs=shot_manager_maya_utils.create_tab()
        for each_tab in tabs:
            asset_manager_layout.addWidget(each_tab[0])
            asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])
