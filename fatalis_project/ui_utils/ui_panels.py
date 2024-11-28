import sys
from PySide6 import QtWidgets, QtCore, QtGui
import qfluentwidgets


class TreePanel(QtWidgets.QFrame):
    """
    Base instance of the ThreePanel Widget, used to show the hierarchy of the project to filter the asset/shots
    in the main tab UI.
    This class should be overridden by subclasses depending on the software or if we are in asset or shot context.
    """
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
        """
        Fill the tree depending on what we except in the context. This is the function that should be overridden.
        """
        pass

class TaskFilterPanel(QtWidgets.QWidget):
    """
    Base instance of the TaskFilterPanel Widget, used to show a list of the task of the project to filter elements
    in the main tab UI.
    This class should be overridden by subclasses depending on the software or if we are in asset or shot context.
    """
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
        """
        define the stands that we want to use to filter elements in the main tab UI depending on the context.
        This is the function that should be overridden.
        :return: list[str] Stands used to filter the tasks.
        """
        stands = [
            "Concept",
            "Modeling",
            "Texturing",
            "Lookdev",
            "Rigging",
            "Layout",
            "Animation",
            "Lighting",
            "Matte",
            "Compositing",
            "Editing",
            "Youping",
        ]
        return stands

class FilterBarPanel(QtWidgets.QWidget):
    """
    Base instance of the FilterBarPanel Widget, used to let the artist filter what he wants in the main tab UI
    by taping in the filter bar.
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet("Demo {background: rgb(32, 32, 32)}")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.lineEdit = qfluentwidgets.SearchLineEdit(self)
        self.button = qfluentwidgets.PushButton('Search', self)

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
    """
    Base instance of the MainTablePanel Widget, used to show the list of assets, dpeending on the filters of the user.
    This class could be overridden by subclasses depending on the software or if we are in asset or shot context if
    needed.
    """
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.tableView = qfluentwidgets.TableWidget(self)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.tableView.setSortingEnabled(True)

        self.tableView.setBorderVisible(True)

        self.define_table_content()
        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        self.hBoxLayout.addWidget(self.tableView)

    def define_table_content(self):
        self.tableView.setRowCount(60)
        self.tableView.setColumnCount(7)
        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(['Asset Name', '.ext', 'Task', 'Version', 'Owner', 'Date', 'Infos'])

        self.tableView.setColumnWidth(0, 250)
        self.tableView.setColumnWidth(1, 65)
        self.tableView.setColumnWidth(2, 100)
        self.tableView.setColumnWidth(3, 65)
        self.tableView.setColumnWidth(4, 100)
        self.tableView.setColumnWidth(5, 80)
        self.tableView.setColumnWidth(6, 100)

    def fill_asset_list(self):
        pass

class InfoPanel(QtWidgets.QWidget):
    """
    Base instance of the InfoPanel Widget, used to show details of the asset selected by the user in the MainTablePanel.
    This class could be overridden by subclasses depending on the software or if we are in asset or shot context if
    needed.
    """
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

        self.tableView.setPlainText(complex_text)
        self.hBoxLayout.addWidget(self.tableView)


class LoadingPanel(QtWidgets.QWidget):
    """
    Base instance of the LoadingPanel Widget, used to add buttons to deal with the elements on the server, for exemple
    to download file/folder, open the selected asset in maya, houdini, or open a Publisher UI.
    This class should be overridden by subclasses depending on the software or if we are in asset or shot context if
    needed.
    """
    def __init__(self):
        super().__init__()
        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.create_buttons()

    def create_buttons(self):
        """
        create the buttons and add it to the LoadingPanel Widget.
        """
        pass
