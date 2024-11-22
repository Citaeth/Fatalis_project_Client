from PySide6 import QtWidgets, QtCore
import qfluentwidgets

from fatalis_project.shot_manager import shot_manager_panels


class MayaShotTreePanel(shot_manager_panels.ShotTreePanel):
    """
    Maya iteration for the ShotTreePanel, override if needed change in maya from the main in asset manager panels.
    """
    def fill_tree(self):
        item1 = QtWidgets.QTreeWidgetItem([self.tr('Shots -')])
        self.tree.addTopLevelItem(item1)


class MayaShotTaskFilterPanel(shot_manager_panels.ShotTaskFilterPanel):
    """
    Maya iteration for the ShotTaskFilterPanel, override if needed change in maya from the main in asset manager panels.
    """
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.listWidget = qfluentwidgets.ListWidget(self)

        stands = [
            "concept",
            "layout",
            "animation",
            "lighting",
            "matte",
            "editing",
            "youping",
        ]
        for stand in stands:
            item = QtWidgets.QListWidgetItem(stand)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)


class MayaShotFilterBarPanel(shot_manager_panels.ShotFilterBarPanel):
    """
    Maya iteration for the ShotFilterBarPanel, override if needed change in maya from the main in asset manager panels.
    """


class MayaShotMainTablePanel(shot_manager_panels.ShotMainTablePanel):
    """
    Maya iteration for the ShotMainTablePanel, override if needed change in maya from the main in asset manager panels.
    """


class MayaShotInfoPanel(shot_manager_panels.ShotInfoPanel):
    """
    Maya iteration for the ShotInfoPanel, override if needed change in maya from the main in asset manager panels.
    """


class MayaShotLoadingPanel(shot_manager_panels.ShotLoadingPanel):
    """
    Maya iteration for the ShotLoadingPanel, override if needed change in maya from the main in asset manager panels.
    """

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QtWidgets.QVBoxLayout(self)

        load_in_maya_button = qfluentwidgets.PushButton('Load Shot in Maya')
        load_in_maya_button.clicked.connect(self.load_shot_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

    def load_shot_in_maya(self):
        print('Loading Shot in Maya')
