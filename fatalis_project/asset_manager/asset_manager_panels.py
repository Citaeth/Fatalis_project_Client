import sys
from PySide6 import QtWidgets, QtCore, QtGui
import qfluentwidgets
import subprocess


import fatalis_project
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


class AssetTaskFilterPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.listWidget = qfluentwidgets.ListWidget(self)

        stands = [
            "concept",
            "modeling",
            "texturing",
            "lookdev",
            "rigging",
            "matte",
            "youping",
        ]
        for stand in stands:
            item = QtWidgets.QListWidgetItem(stand)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)


class AssetFilterBarPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("Demo {background: rgb(32, 32, 32)}")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.lineEdit = qfluentwidgets.SearchLineEdit(self)
        self.button = qfluentwidgets.PushButton('Search', self)

        # add completer
        stands = [
            "concept",
            "modeling",
            "texturing",
            "lookdev",
            "rigging",
            "layout",
            "animation",
            "lighting",
            "matte",
            "compositing",
            "editing",
            "youping",
        ]
        self.completer = QtWidgets.QCompleter(stands, self.lineEdit)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.lineEdit.setCompleter(self.completer)

        self.hBoxLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.lineEdit, 1)
        self.hBoxLayout.addWidget(self.button, 0, QtCore.Qt.AlignCenter)

        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Search stand')


class AssetMainTablePanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.tableView = qfluentwidgets.TableWidget(self)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        # enable border
        self.tableView.setBorderVisible(True)

        self.tableView.setRowCount(60)
        self.tableView.setColumnCount(6)
        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(['Asset', 'Type', 'Version', 'Owner', 'Date', 'Infos'])

        self.tableView.setColumnWidth(0, 250)
        self.tableView.setColumnWidth(1, 100)
        self.tableView.setColumnWidth(2, 65)
        self.tableView.setColumnWidth(3, 100)
        self.tableView.setColumnWidth(4, 80)
        self.tableView.setColumnWidth(5, 100)

        assets_infos = [
        ]
        assets_infos += assets_infos
        for i, asset_info in enumerate(assets_infos):
            for j in range(6):
                self.tableView.setItem(i, j, QtWidgets.QTableWidgetItem(asset_info[j]))

        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        self.hBoxLayout.addWidget(self.tableView)


class AssetInfoPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setStretch(0, 1)

        self.tableView = qfluentwidgets.TextEdit(self)
        self.tableView.setReadOnly(True)
        complex_text = """Coucou ceci est un espace info

                Il y aura beaucoup de choses et elements dedans

                - Petit element 1
                - Petit element 2

                et pleeeeins d'autres ensuite."""

        # Définir le texte dans le QTextEdit
        self.tableView.setPlainText(complex_text)

        self.hBoxLayout.addWidget(self.tableView)


class AssetLoadingPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.vBoxLayout = QtWidgets.QVBoxLayout(self)

        load_in_maya_button=qfluentwidgets.PushButton('Load Asset in Maya')
        load_in_maya_button.clicked.connect(self.load_asset_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

        load_in_houdini_button = qfluentwidgets.PushButton('Load Asset in Houdini')
        load_in_houdini_button.clicked.connect(self.load_asset_in_houdini)
        self.vBoxLayout.addWidget(load_in_houdini_button)

    def load_asset_in_maya(self):
        print('Loading Asset in Maya')

        user_config = ui_utils.get_user_config_file()
        maya_path = user_config.find('./software/maya/path').text

        try:
            subprocess.Popen([maya_path])
        except FileNotFoundError:
            print("the maya path is wrong, please check it.")
        except Exception as e:
            print(f"error during launching maya : {e}")


    def load_asset_in_houdini(self):
        print('Loading Asset in Houdini')

        user_config = ui_utils.get_user_config_file()
        houdini_path = user_config.find('./software/houdini/path').text

        try:
            subprocess.Popen([houdini_path])
        except FileNotFoundError:
            print("the houdini path is wrong, please check it.")
        except Exception as e:
            print(f"error during launching houdini : {e}")
