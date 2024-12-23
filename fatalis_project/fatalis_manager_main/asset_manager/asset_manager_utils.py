from PySide6 import QtWidgets, QtCore
import textwrap
from fatalis_project.fatalis_manager_main.asset_manager import asset_manager_panels as panels

def create_tab(database_assets_infos):
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

    asset_filter_widget = panels.AssetTreePanel(True)
    task_filter_widget = panels.AssetTaskFilterPanel()
    asset_filter_widget.tree.itemChanged.connect(lambda: apply_filters_on_main_table(filter_bar_widget,
                                                                                     asset_filter_widget,
                                                                                     task_filter_widget,
                                                                                     main_table_widget))
    task_filter_widget.listWidget.itemChanged.connect(lambda: apply_filters_on_main_table(filter_bar_widget,
                                                                                          asset_filter_widget,
                                                                                          task_filter_widget,
                                                                                          main_table_widget))
    left_tab_layout.addWidget(asset_filter_widget)
    left_tab_layout.addWidget(task_filter_widget)

    left_tab_layout.setStretch(0, 3)
    left_tab_layout.setStretch(1, 2)

    # Mid tab, created before because the Left tab is supposed to contain filter widget for the main table in the mid.
    mid_tab = QtWidgets.QWidget()
    mid_tab_layout = QtWidgets.QVBoxLayout(mid_tab)
    mid_tab.setLayout(mid_tab_layout)
    filter_bar_widget = panels.AssetFilterBarPanel()
    filter_bar_widget.search_button.clicked.connect(lambda: apply_filters_on_main_table(filter_bar_widget,
                                                                                        asset_filter_widget,
                                                                                        task_filter_widget,
                                                                                        main_table_widget))
    mid_tab_layout.addWidget(filter_bar_widget)
    main_table_widget = panels.AssetMainTablePanel()
    main_table_widget.update_table_with_asset_database(database_assets_infos)
    main_table_widget.tableView.itemSelectionChanged.connect(lambda:fill_info_selected_in_table(main_table_widget, info_widget))
    mid_tab_layout.addWidget(main_table_widget)
    mid_tab_layout.setStretch(0, 0)
    mid_tab_layout.setStretch(1, 3)

    # Right tab
    right_tab = QtWidgets.QWidget()
    right_tab_layout = QtWidgets.QVBoxLayout(right_tab)
    right_tab.setLayout(right_tab_layout)
    info_widget = panels.AssetInfoPanel()
    right_tab_layout.addWidget(info_widget)
    load_buttons_widget = panels.AssetLoadingPanel(main_table_widget)

    right_tab_layout.addWidget(load_buttons_widget)
    right_tab_layout.setStretch(0, 1)

    tabs.append([left_tab, 0])
    tabs.append([mid_tab, 3])
    tabs.append([right_tab, 1])
    return tabs


def fill_info_selected_in_table(table_widget, info_widget):
    """
    fill the info widget at the right of the UI with the information of the selected asset in the main table.
    :param table_widget: widget of the table where the assets are listed.
    :param info_widget: widget showing the infos of the selected asset in the main table.
    """
    selected_items = table_widget.tableView.selectedItems()
    if selected_items:
        selected_row = selected_items[0].row()
        row_data = [table_widget.tableView.item(selected_row, col).text() for col in range(table_widget.tableView.columnCount())]
        infos = textwrap.dedent(f"""\
        {row_data[0]};
        Task: {row_data[2]}; Version: {row_data[3]};
        File type: {row_data[1]};
        Owner: {row_data[4]};
        Date: {row_data[5]};

        Infos: {row_data[6]};""")
        info_widget.tableView.setPlainText(infos)


def apply_filters_on_main_table(search_bar, asset_filter, task_filter, main_table_widget):
    """
    Apply the filter from Assets List, Task List and the search bar to the main table.
    :param search_bar:
    :param asset_filter:
    :param task_filter:
    :param main_table_widget:
    :return:
    """
    checked_tasks = []
    assets_selected = []

    iterator = QtWidgets.QTreeWidgetItemIterator(asset_filter.tree)
    while iterator.value():
        item = iterator.value()
        if item.checkState(0) == QtCore.Qt.CheckState.Checked:
            assets_selected.append(item.text(0))
        iterator += 1

    for index in range(task_filter.listWidget.count()):
        item = task_filter.listWidget.item(index)
        if item.checkState() == QtCore.Qt.CheckState.Checked:
            checked_tasks.append(item.text())

    for row in range(main_table_widget.tableView.rowCount()):
        asset_name = main_table_widget.tableView.item(row, 0).text()
        task_name = main_table_widget.tableView.item(row, 2).text()
        if not assets_selected:
            main_table_widget.tableView.setRowHidden(row, False)
        for asset_filter in assets_selected:
            if asset_filter.lower() in asset_name.lower() or 'Assets - ' in assets_selected:
                main_table_widget.tableView.setRowHidden(row, False)
                break
            else:
                main_table_widget.tableView.setRowHidden(row, True)
        if not task_name in checked_tasks and not checked_tasks==[]:
            main_table_widget.tableView.setRowHidden(row, True)
        if main_table_widget.tableView.item(row + 1, 0) is None:
            break

    if not search_bar.lineEdit.text():
        return
    search_bar_asset=[]
    for row in range(main_table_widget.tableView.rowCount()):
        for column_index in range(main_table_widget.tableView.columnCount()):
            column_content = main_table_widget.tableView.item(row, column_index)
            if not column_content:
                search_bar_asset.append(row)
                break
            elif search_bar.lineEdit.text().lower() in column_content.text().lower():
                search_bar_asset.append(row)
        if not row in search_bar_asset:
            main_table_widget.tableView.setRowHidden(row, True)
