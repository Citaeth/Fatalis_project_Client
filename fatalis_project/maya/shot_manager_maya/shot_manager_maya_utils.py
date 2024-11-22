from PySide6 import QtWidgets

from fatalis_project.maya.shot_manager_maya import shot_manager_maya_panels as panels


def create_tab():
    """
    create and fill different tabs into the Shot Manager.
    The current function define the tabs for the Asset Manager in the Fatalis Project main UI, and could be
    overridden in the ShotManagerApplication versions in software.
    :return list tabs: list the tabs wanted in the app, and their stretch factor.
    """
    tabs = []
    # Left tab
    left_tab = QtWidgets.QWidget()
    left_tab_layout = QtWidgets.QVBoxLayout(left_tab)
    left_tab.setLayout(left_tab_layout)
    left_tab_layout.addWidget(panels.MayaShotTreePanel(True))
    left_tab_layout.addWidget(panels.MayaShotTaskFilterPanel())
    left_tab_layout.setStretch(0, 3)
    left_tab_layout.setStretch(1, 2)
    tabs.append([left_tab, 0])

    # Mid tab
    mid_tab = QtWidgets.QWidget()
    mid_tab_layout = QtWidgets.QVBoxLayout(mid_tab)
    mid_tab.setLayout(mid_tab_layout)
    mid_tab_layout.addWidget(panels.MayaShotFilterBarPanel())
    mid_tab_layout.addWidget(panels.MayaShotMainTablePanel())
    mid_tab_layout.setStretch(0, 0)
    mid_tab_layout.setStretch(1, 3)
    tabs.append([mid_tab, 3])

    # Right tab
    right_tab = QtWidgets.QWidget()
    right_tab_layout = QtWidgets.QVBoxLayout(right_tab)
    right_tab.setLayout(right_tab_layout)
    right_tab_layout.addWidget(panels.MayaShotInfoPanel())
    right_tab_layout.addWidget(panels.MayaShotLoadingPanel())
    right_tab_layout.setStretch(0, 1)
    tabs.append([right_tab, 1])

    return tabs