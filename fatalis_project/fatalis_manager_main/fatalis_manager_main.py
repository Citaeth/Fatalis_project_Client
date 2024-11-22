import sys
from PySide6 import QtWidgets, QtGui
import qfluentwidgets

from fatalis_project.asset_manager.asset_manager_ui import AssetManagerInterface
from fatalis_project.shot_manager.shot_manager_ui import ShotManagerInterface
from fatalis_project.reference_gallery.reference_gallery_ui import ReferenceGalleryInterface

class FatalisManagerMain(qfluentwidgets.FluentWindow):
    """
    Main Class of the Fatalis Project UI, outside any software.
    Should allow you to access to any stuff build for this project (for now, only the asset manager)
    """
    def __init__(self):
        super(FatalisManagerMain, self).__init__()
        self.setWindowTitle('Fatalis Project')
        self.setWindowIcon(QtGui.QIcon(':/qfluentwidgets/images/icons/Calories_white.svg'))
        qfluentwidgets.setTheme(qfluentwidgets.Theme.DARK)
        qfluentwidgets.setThemeColor("#8e3838", save=False)
        self.resize(1500, 850)
        self.add_navigations_interface()
        self.force_refresh()


    def add_navigations_interface(self):
        self.navigationInterface.addSeparator()
        self.asset_manager_interface = AssetManagerInterface(self)
        self.addSubInterface(self.asset_manager_interface, text='Asset Manager', icon=qfluentwidgets.FluentIcon.FOLDER)

        self.shot_manager_interface = ShotManagerInterface(self)
        self.addSubInterface(self.shot_manager_interface,
                             text='Shot Manager',
                             icon=qfluentwidgets.FluentIcon.VIDEO)

        self.references_gallery = ReferenceGalleryInterface(self)
        self.addSubInterface(self.references_gallery,
                             text="Story Gallery",
                             position=qfluentwidgets.NavigationItemPosition.BOTTOM,
                             icon=qfluentwidgets.FluentIcon.LIBRARY_FILL
                             )

        self.navigationInterface.setExpandWidth(200)

    def force_refresh(self):
        """
        refresh the UI, using the data on the server.
        """
        pass


if __name__ == '__main__':
    """
    loading the UI when calling the file.
    """
    app = QtWidgets.QApplication(sys.argv)
    w = FatalisManagerMain()
    w.show()
    app.exec()
