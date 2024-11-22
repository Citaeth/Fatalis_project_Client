from PySide6 import QtWidgets
import qfluentwidgets
import subprocess

from fatalis_project.ui_utils import ui_panels, ui_utils


class AssetTreePanel(ui_panels.TreePanel):
    def fill_tree(self):
        item1 = QtWidgets.QTreeWidgetItem([self.tr('Assets - ')])
        item1.addChildren([
            QtWidgets.QTreeWidgetItem([self.tr('Asset_01')]),
            QtWidgets.QTreeWidgetItem([self.tr('Asset_02')]),
            QtWidgets.QTreeWidgetItem([self.tr('Asset_03')]),
        ])
        self.tree.addTopLevelItem(item1)


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


class AssetInfoPanel(ui_panels.InfoPanel):
    """

    """


class AssetLoadingPanel(ui_panels.LoadingPanel):
    """

    """
    def create_buttons(self):
        load_in_maya_button = qfluentwidgets.PushButton('Load Asset in Maya')
        load_in_maya_button.clicked.connect(self.load_asset_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

        load_in_houdini_button = qfluentwidgets.PushButton('Load Asset in Houdini')
        load_in_houdini_button.clicked.connect(self.load_asset_in_houdini)
        self.vBoxLayout.addWidget(load_in_houdini_button)


    def load_asset_in_maya(self):
        user_config = ui_utils.get_user_config_file()
        maya_path = user_config.find('./software/maya/path').text

        try:
            subprocess.Popen([maya_path])
        except FileNotFoundError:
            print("the maya path is wrong, please check it.")
        except Exception as e:
            print(f"error during launching maya : {e}")


    def load_asset_in_houdini(self):
        user_config = ui_utils.get_user_config_file()
        houdini_path = user_config.find('./software/houdini/path').text

        try:
            subprocess.Popen([houdini_path])
        except FileNotFoundError:
            print("the houdini path is wrong, please check it.")
        except Exception as e:
            print(f"error during launching houdini : {e}")
