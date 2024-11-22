from PySide6 import QtWidgets
import qfluentwidgets
import subprocess

from fatalis_project.ui_utils import ui_panels, ui_utils


class ShotTreePanel(ui_panels.TreePanel):
    def fill_tree(self):
        item1 = QtWidgets.QTreeWidgetItem([self.tr('Shots -')])
        item11 = QtWidgets.QTreeWidgetItem([self.tr('FXs')])
        item11.addChildren([
            QtWidgets.QTreeWidgetItem(['BOUM']),
            QtWidgets.QTreeWidgetItem(['BIM']),
            QtWidgets.QTreeWidgetItem(['BAM']),
            QtWidgets.QTreeWidgetItem(['PFIOUUU']),
        ])
        item1.addChild(item11)
        self.tree.addTopLevelItem(item1)


class ShotTaskFilterPanel(ui_panels.TaskFilterPanel):
    def define_stand(self):
        stands = [
            "concept",
            "layout",
            "animation",
            "lighting",
            "matte",
            "compositing",
            "editing",
            "youping",
        ]
        return stands


class ShotFilterBarPanel(ui_panels.FilterBarPanel):
    """
    """


class ShotMainTablePanel(ui_panels.MainTablePanel):
    """

    """


class ShotInfoPanel(ui_panels.InfoPanel):
    """

    """


class ShotLoadingPanel(ui_panels.LoadingPanel):
    def create_buttons(self):
        load_in_maya_button = qfluentwidgets.PushButton('Open Shot in Maya')
        load_in_maya_button.clicked.connect(self.load_asset_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

        load_in_houdini_button = qfluentwidgets.PushButton('Open Shot in Houdini')
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
