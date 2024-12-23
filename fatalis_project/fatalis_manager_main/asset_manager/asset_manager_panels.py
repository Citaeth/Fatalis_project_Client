from PySide6 import QtWidgets, QtCore
import qfluentwidgets
import subprocess

from fatalis_project.ui_utils import ui_panels, utils, publisher_main
from fatalis_project.ui_utils.http_request import read_data_base, change_asset_status, download_main

class AssetTreePanel(ui_panels.TreePanel):
    """
    Base instance of the ThreePanel Widget, used to show the list of the assets in the project,  to filter the content
    of the main table.
    """
    def fill_tree(self):
        """
        Fill the tree with the list of assets of the show.
        """
        item_assets = QtWidgets.QTreeWidgetItem([self.tr('Assets - ')])
        user_config = utils.get_user_config_file()[0]
        asset_list = user_config.find('./assets/name').text.split(", ")
        for each_asset in asset_list:
            item_assets.addChild(QtWidgets.QTreeWidgetItem([self.tr(each_asset)]))
        self.tree.addTopLevelItem(item_assets)


class AssetTaskFilterPanel(ui_panels.TaskFilterPanel):
    """
    Asset instance of the TaskFilterPanel Widget, used to show a list of the task of the project to filter elements
    in the main table.
    """
    def define_stand(self):
        """
        Override and return the stand list, to only have the assets related ones.
        Youping is OF COURSE the most important of them. We should have fun. Youpi. right?
        :return list stands:
        """
        stands = [
            "Concept",
            "Modeling",
            "Texturing",
            "Lookdev",
            "Rigging",
            "Matte",
            "Youping",
        ]
        return stands


class AssetFilterBarPanel(ui_panels.FilterBarPanel):
    """
    Asset instance of the FilterBarPanel Widget, used to let the artist filter the assets in the main table
    by taping in the filter bar.
    """

class AssetMainTablePanel(ui_panels.MainTablePanel):
    """
    Asset instance of the MainTablePanel Widget, used to show the list of assets, depending on the filters of the user.
    Add the information needed to return the info needed in an Asset context, and update the table using the assets
    database.
    """
    dict_asset={
        'name': 0,
        'extension': 1,
        'task': 2,
        'version': 3,
        'user_id': 4,
        'created_at': 5,
        'description': 6,
        'id':7,
        'status':8
    }

    def update_table_with_asset_database(self, database_assets_infos):
        """
        update the main table with the asset database information.
        :param dict database_assets_infos:
        :return:
        """
        users_config = utils.get_project_users_config_file()[1]
        user_id_to_username = {
            user.find('ID').text: user.find("Username").text if user.find("Username") is not None else ''
            for user in users_config.findall('User') if user.find('ID') is not None
        }

        row = 0
        for row_data in database_assets_infos:
            for data_type, column_number in self.dict_asset.items():
                data_base_info = str(row_data.get(data_type))

                if data_type == 'user_id' and data_base_info in user_id_to_username:
                    data_base_info = user_id_to_username[data_base_info]

                item = QtWidgets.QTableWidgetItem(str(data_base_info))
                self.tableView.setItem(row, column_number, item)

            row += 1

    def refresh_table(self):
        """
        refresh the table content, by reading the asset database from the server, in case some update have been made.
        """
        assets_database_infos = read_data_base.get_assets_from_database()
        self.update_table_with_asset_database(assets_database_infos)

    def change_status(self, asset_id, status):
        """
        function to change the status of selected version.
        :param int asset_id: ID of the asset that should change its status. Need to send the information to server.
        :param str status: new status of the asset version.
        :param asset_id:
        :param status:
        :return:
        """
        change_asset_status.change_asset_status(asset_id, status)
        self.refresh_table()

class AssetInfoPanel(ui_panels.InfoPanel):
    """
    Asset instance of the InfoPanel Widget, used to show details of the asset selected by the user in the MainTablePanel.
    """


class AssetLoadingPanel(ui_panels.LoadingPanel):
    """
    Asset instance of the LoadingPanel Widget, used to add buttons to deal with the elements on the server, for exemple
    to download file/folder, open the selected asset in maya, houdini, or open a Publisher UI, in an assets context.
    """

    def create_buttons(self):
        """
        create the buttons and add it to the LoadingPanel Widget.
        """
        self.download_button = qfluentwidgets.PushButton('Download File / Folder')
        self.vBoxLayout.addWidget(self.download_button)
        self.download_button.clicked.connect(self.download_files)

        load_in_maya_button = qfluentwidgets.PushButton('Open Maya')
        load_in_maya_button.clicked.connect(self.load_asset_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

        load_in_houdini_button = qfluentwidgets.PushButton('Open Houdini')
        load_in_houdini_button.clicked.connect(self.load_asset_in_houdini)
        self.vBoxLayout.addWidget(load_in_houdini_button)

        publish_on_server_button = qfluentwidgets.PushButton('Publish on server')
        publish_on_server_button.clicked.connect(publisher_main.open_publisher)
        self.vBoxLayout.addWidget(publish_on_server_button)

    def download_files(self):
        """
        download the selected file(s) in the UI from the server.
        :param table_widget:
        :return:
        """
        selected_items = self.table_widget.tableView.selectedItems()
        if not selected_items:
            qfluentwidgets.InfoBar.warning('Download Issue',
                                           'Please select something to download in the table!',
                                           orient=QtCore.Qt.Vertical,
                                           isClosable=True,
                                           duration=2000,
                                           parent=self.table_widget)
            return
        dest_folder_widget = QtWidgets.QWidget()
        folder = QtWidgets.QFileDialog.getExistingDirectory(dest_folder_widget, "Select Download Directory")
        if folder:
            download_path = folder
            selected_row = selected_items[0].row()
            asset_id = self.table_widget.tableView.item(selected_row, 7).text()
            download_main.download_from_server(asset_id, download_path)

    def load_asset_in_maya(self):
        """
        Open maya using the path found in the config file, or running the process to find the path first.
        TODO: Implement the "Open asset as..." feature.
        """
        user_config_root, user_config_tree, user_config_path = utils.get_user_config_file()
        maya_path = user_config_root.find('./software/maya/path').text
        if not maya_path:
            maya_path = self.get_maya_path(user_config_root, user_config_tree, user_config_path)
        try:
            subprocess.Popen([maya_path])
        except FileNotFoundError:
            print("the maya path is wrong, please check it.")
        except Exception as e:
            print(f"error during launching maya : {e}")


    def load_asset_in_houdini(self):
        """
        Open houdini using the path found in the config file, or running the process to find the path first.
        TODO: Implement the "Open asset as..." feature.
        """
        user_config_root, user_config_tree, user_config_path = utils.get_user_config_file()
        houdini_path = user_config_root.find('./software/houdini/path').text
        if not houdini_path:
            houdini_path = self.get_houdini_path(user_config_root, user_config_tree, user_config_path)
        try:
            subprocess.Popen([houdini_path])
        except FileNotFoundError:
            print("the houdini path is wrong, please check it.")
        except Exception as e:
            print(f"error during launching houdini : {e}")
