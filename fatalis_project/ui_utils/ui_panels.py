import sys
from PySide6 import QtWidgets, QtCore, QtGui
import qfluentwidgets


class TreePanel(QtWidgets.QFrame):
    def __init__(self, enable_check=False):
        super().__init__()
        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.tree = qfluentwidgets.TreeWidget(self)
        self.hBoxLayout.addWidget(self.tree)

        self.fill_tree()
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)

        if enable_check:
            it = QtWidgets.QTreeWidgetItemIterator(self.tree)
            while(it.value()):
                it.value().setCheckState(0, QtCore.Qt.Unchecked)
                it += 1

    def fill_tree(self):
        pass

class TaskFilterPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.listWidget = qfluentwidgets.ListWidget(self)

        stands = self.define_stand()
        for stand in stands:
            item = QtWidgets.QListWidgetItem(stand)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)

    def define_stand(self):
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
        return stands

class FilterBarPanel(QtWidgets.QWidget):
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


class MainTablePanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.tableView = qfluentwidgets.TableWidget(self)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        # enable border
        self.tableView.setBorderVisible(True)

        self.define_table_content()

        assets_infos = [
        ]
        assets_infos += assets_infos
        for i, asset_info in enumerate(assets_infos):
            for j in range(6):
                self.tableView.setItem(i, j, QtWidgets.QTableWidgetItem(asset_info[j]))

        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        self.hBoxLayout.addWidget(self.tableView)

    def define_table_content(self):
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


class InfoPanel(QtWidgets.QWidget):
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


class LoadingPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.create_buttons()

    def create_buttons(self):
        load_in_maya_button = qfluentwidgets.PushButton('Load Asset in Maya')
        load_in_maya_button.clicked.connect(self.load_asset_in_maya)
        self.vBoxLayout.addWidget(load_in_maya_button)

        load_in_houdini_button = qfluentwidgets.PushButton('Load Asset in Houdini')
        load_in_houdini_button.clicked.connect(self.load_asset_in_houdini)
        self.vBoxLayout.addWidget(load_in_houdini_button)

    def load_asset_in_maya(self):
        pass

    def load_asset_in_houdini(self):
        pass
