from PySide6 import QtWidgets
import qfluentwidgets
import subprocess

from fatalis_project.ui_utils import ui_panels, utils, publisher_main
from fatalis_project.ui_utils.http_request import read_data_base, change_asset_status


class AssetTreePanel(ui_panels.TreePanel):
    def fill_tree(self):
        item_assets = QtWidgets.QTreeWidgetItem([self.tr('Assets - ')])
        user_config = utils.get_user_config_file()[0]
        asset_list = user_config.find('./assets/name').text.split(", ")
        for each_asset in asset_list:
            item_assets.addChild(QtWidgets.QTreeWidgetItem([self.tr(each_asset)]))
        self.tree.addTopLevelItem(item_assets)


class AssetTaskFilterPanel(ui_panels.TaskFilterPanel):
    def define_stand(self):
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
        'description': 6,
        'id':7,
        'status':8
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

    def refresh_table(self):
        assets_database_infos = read_data_base.get_assets_from_database()
        self.update_table_with_asset_database(assets_database_infos)

    def change_status(self, asset_id, status):
        print('change asset {} status into {}'.format(asset_id, status))
        change_asset_status.change_asset_status(asset_id, status)
        self.refresh_table()

class AssetInfoPanel(ui_panels.InfoPanel):
    """

    """


class AssetLoadingPanel(ui_panels.LoadingPanel):
    """

    """
    def create_buttons(self):
        self.download_button = qfluentwidgets.PushButton('Download File / Folder')
        self.vBoxLayout.addWidget(self.download_button)

        load_in_maya_button = qfluentwidgets.PushButton('Open Maya')
        load_in_maya_button.clicked.connect(self.load_asset_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

        load_in_houdini_button = qfluentwidgets.PushButton('Open Houdini')
        load_in_houdini_button.clicked.connect(self.load_asset_in_houdini)
        self.vBoxLayout.addWidget(load_in_houdini_button)

        publish_on_server_button = qfluentwidgets.PushButton('Publish on server')
        publish_on_server_button.clicked.connect(publisher_main.open_publisher)
        self.vBoxLayout.addWidget(publish_on_server_button)


    def download_folder_file(self):
        pass

    def load_asset_in_maya(self):
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
