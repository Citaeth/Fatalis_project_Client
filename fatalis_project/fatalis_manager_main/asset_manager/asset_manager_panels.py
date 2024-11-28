from PySide6 import QtWidgets
import qfluentwidgets
import subprocess

from fatalis_project.ui_utils import ui_panels, utils, publisher_main


class AssetTreePanel(ui_panels.TreePanel):
    def fill_tree(self):
        item_assets = QtWidgets.QTreeWidgetItem([self.tr('Assets - ')])
        user_config = utils.get_user_config_file()
        asset_list = user_config.find('./assets/name').text.split(", ")
        for each_asset in asset_list:
            item_assets.addChild(QtWidgets.QTreeWidgetItem([self.tr(each_asset)]))
        self.tree.addTopLevelItem(item_assets)


class AssetTaskFilterPanel(ui_panels.TaskFilterPanel):
    def define_stand(self):
        stands = [
            "concept",
            "modeling",
            "texturing",
            "lookdev",
            "rigging",
            "matte",
            "youping",
        ]
        return stands


class AssetFilterBarPanel(ui_panels.FilterBarPanel):
    """

    """

class AssetMainTablePanel(ui_panels.MainTablePanel):
    """
    """
    dict_asset={
        'name': 0,
        'extension': 1,
        'task': 2,
        'version': 3,
        'user_id': 4,
        'created_at': 5,
        'description': 6
    }

    def update_table_with_asset_database(self, database_assets_infos):
        row = 0
        users_config = utils.get_project_users_config_file()[1]
        for row_data in database_assets_infos:
            for data_type in self.dict_asset:
                data_base_info = database_assets_infos[row][data_type]
                column_number = self.dict_asset[data_type]
                if data_type=='user_id':
                    for user in users_config.findall('User'):
                        id_element = user.find('ID')
                        if id_element is not None and id_element.text == str(data_base_info):
                            username_element = user.find("Username").text if user.find("Username") is not None else ''
                            data_base_info = username_element
                item = QtWidgets.QTableWidgetItem(str(data_base_info))
                self.tableView.setItem(row, column_number, item)
            row = row + 1


class AssetInfoPanel(ui_panels.InfoPanel):
    """

    """


class AssetLoadingPanel(ui_panels.LoadingPanel):
    """

    """
    def create_buttons(self):
        download_button = qfluentwidgets.PushButton('Dowmload File / Folder')
        download_button.clicked.connect(self.download_folder_file)
        self.vBoxLayout.addWidget(download_button)

        load_in_maya_button = qfluentwidgets.PushButton('Load Asset in Maya')
        load_in_maya_button.clicked.connect(self.load_asset_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

        load_in_houdini_button = qfluentwidgets.PushButton('Load Asset in Houdini')
        load_in_houdini_button.clicked.connect(self.load_asset_in_houdini)
        self.vBoxLayout.addWidget(load_in_houdini_button)

        publish_on_server_button = qfluentwidgets.PushButton('Publish on server')
        publish_on_server_button.clicked.connect(publisher_main.open_publisher)
        self.vBoxLayout.addWidget(publish_on_server_button)


    def download_folder_file(self):
        pass

    def load_asset_in_maya(self):
        user_config = utils.get_user_config_file()
        maya_path = user_config.find('./software/maya/path').text

        try:
            subprocess.Popen([maya_path])
        except FileNotFoundError:
            print("the maya path is wrong, please check it.")
        except Exception as e:
            print(f"error during launching maya : {e}")


    def load_asset_in_houdini(self):
        user_config = utils.get_user_config_file()
        houdini_path = user_config.find('./software/houdini/path').text

        try:
            subprocess.Popen([houdini_path])
        except FileNotFoundError:
            print("the houdini path is wrong, please check it.")
        except Exception as e:
            print(f"error during launching houdini : {e}")
