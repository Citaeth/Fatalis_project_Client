from PySide6 import QtWidgets, QtCore

from fatalis_project.fatalis_manager_main.asset_manager import asset_manager_panels as panels


def create_tab(database_assets_infos):
    """
    create and fill different tabs into the Shot Manager.
    The current function define the tabs for the Asset Manager in the Fatalis Project main UI, and could be
    overridden in the ShotManagerApplication versions in software.
    :return list tabs: list the tabs wanted in the app, and their stretch factor.
    """
    tabs = []

    # Right tab Create before because InfoPanel should be updated when selecting an element in MainTable
    right_tab = QtWidgets.QWidget()
    right_tab_layout = QtWidgets.QVBoxLayout(right_tab)
    right_tab.setLayout(right_tab_layout)
    info_widget = panels.AssetInfoPanel()
    right_tab_layout.addWidget(info_widget)
    right_tab_layout.addWidget(panels.AssetLoadingPanel())
    right_tab_layout.setStretch(0, 1)

    # Mid tab, created before because the Left tab is supposed to contain filter widget for the main table in the mid.
    mid_tab = QtWidgets.QWidget()
    mid_tab_layout = QtWidgets.QVBoxLayout(mid_tab)
    mid_tab.setLayout(mid_tab_layout)
    mid_tab_layout.addWidget(panels.AssetFilterBarPanel())
    main_table_widget = panels.AssetMainTablePanel()
    main_table_widget.update_table_with_asset_database(database_assets_infos)
    main_table_widget.tableView.itemSelectionChanged.connect(lambda:fill_info_selected_in_table(main_table_widget, info_widget))
    mid_tab_layout.addWidget(main_table_widget)
    mid_tab_layout.setStretch(0, 0)
    mid_tab_layout.setStretch(1, 3)

    # Left tab
    left_tab = QtWidgets.QWidget()
    left_tab_layout = QtWidgets.QVBoxLayout(left_tab)
    left_tab.setLayout(left_tab_layout)

    asset_filter_widget = panels.AssetTreePanel(True)
    task_filter_widget = panels.AssetTaskFilterPanel()
    asset_filter_widget.tree.itemChanged.connect(lambda: apply_filters_on_main_table(asset_filter_widget,
                                                                                     task_filter_widget,
                                                                                     main_table_widget))
    task_filter_widget.listWidget.itemChanged.connect(lambda: apply_filters_on_main_table(asset_filter_widget,
                                                                                          task_filter_widget,
                                                                                          main_table_widget))
    left_tab_layout.addWidget(asset_filter_widget)
    left_tab_layout.addWidget(task_filter_widget)

    left_tab_layout.setStretch(0, 3)
    left_tab_layout.setStretch(1, 2)

    tabs.append([left_tab, 0])
    tabs.append([mid_tab, 3])
    tabs.append([right_tab, 1])
    return tabs


def fill_info_selected_in_table(table_widget, info_widget):
    selected_items = table_widget.tableView.selectedItems()
    if selected_items:
        selected_row = selected_items[0].row()  # Obtenir l'index de la ligne sélectionnée
        row_data = [table_widget.tableView.item(selected_row, col).text() for col in range(table_widget.tableView.columnCount())]
        infos = """{};
                Task: {}; Version: {};
                File type: {};
                owner: {};
                date: {};
                   
                infos: {};""".format(row_data[0], row_data[2], row_data[3], row_data[1], row_data[4], row_data[5], row_data[6])
        info_widget.tableView.setPlainText(infos)


def apply_filters_on_main_table(asset_filter, task_filter, main_table_widget):
    checked_tasks = []
    assets_selected = []

    iterator = QtWidgets.QTreeWidgetItemIterator(asset_filter.tree)
    while iterator.value():
        item = iterator.value()
        if item.checkState(0) == QtCore.Qt.CheckState.Checked:
            assets_selected.append(item.text(0))
        iterator += 1

    for index in range(task_filter.listWidget.count()):
        item = task_filter.listWidget.item(index)  # Récupérer l'élément
        if item.checkState() == QtCore.Qt.CheckState.Checked:
            checked_tasks.append(item.text())

    for row in range(main_table_widget.tableView.rowCount()):
        asset_name = main_table_widget.tableView.item(row, 0).text()
        task_name = main_table_widget.tableView.item(row, 2).text()
        if not assets_selected:
            main_table_widget.tableView.setRowHidden(row, False)
        for asset_filter in assets_selected:
            if asset_filter in asset_name or 'Assets - ' in assets_selected:
                main_table_widget.tableView.setRowHidden(row, False)
                break
            else:
                main_table_widget.tableView.setRowHidden(row, True)
        if not task_name in checked_tasks and not checked_tasks==[]:
            main_table_widget.tableView.setRowHidden(row, True)
        if main_table_widget.tableView.item(row + 1, 0) is None:
            break
