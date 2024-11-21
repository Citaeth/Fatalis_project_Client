from PySide6 import QtWidgets

from fatalis_project.shot_manager import shot_manager_utils
from fatalis_project.ui_utils import ui_utils as utils


class ShotManagerInterface(utils.SingleDirectionScrollInterface):
    """
    The Asset Manager Interface is a Widget who contain the Shot Manager.
    Should be called in the Fatalis Project main UI. It could be bypassed in the Shot Manager in the software, calling
    directly the ShotManagerApplication.
    """
    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.setObjectName('Shot Manager Interface')
        self.appShotManager = ShotManagerApplication(self)
        self.vBoxLayout.addWidget(self.appShotManager)

class ShotManagerApplication(QtWidgets.QWidget):
    """

    """
    def __init__(self, parent=None):
        super(ShotManagerApplication, self).__init__(parent=None)

        asset_manager_layout = QtWidgets.QHBoxLayout()
        self.setLayout(asset_manager_layout)

        tabs=shot_manager_utils.create_tab()
        for each_tab in tabs:
            asset_manager_layout.addWidget(each_tab[0])
            asset_manager_layout.setStretchFactor(each_tab[0], each_tab[1])
