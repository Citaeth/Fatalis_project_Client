import sys
from PySide6 import QtWidgets, QtCore, QtGui
import qfluentwidgets

from fatalis_project.ui_utils import ui_panels


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


class ShotTaskFilterPanel(QtWidgets.QWidget):
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
            "compositing",
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


class ShotFilterBarPanel(QtWidgets.QWidget):
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


class ShotMainTablePanel(QtWidgets.QWidget):
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
        self.tableView.setHorizontalHeaderLabels(['Shot Scene', 'Type', 'Version', 'Owner', 'Date', 'Infos'])

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


class ShotInfoPanel(QtWidgets.QWidget):
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


class ShotLoadingPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.vBoxLayout = QtWidgets.QVBoxLayout(self)

        self.vBoxLayout.addWidget(qfluentwidgets.PushButton('Open Shot in Maya'))
        self.vBoxLayout.addWidget(qfluentwidgets.PushButton('Open Shot in Houdini'))
