import sys
from PySide6 import QtWidgets, QtGui
import qfluentwidgets

from fatalis_project.fatalis_manager_main import fatalis_manager_main
from fatalis_project.maya.asset_manager_maya.asset_manager_maya import AssetManagerInterfaceMaya
from fatalis_project.maya.shot_manager_maya.shot_manager_maya_ui import ShotManagerInterfaceMaya

from fatalis_project.reference_gallery.reference_gallery_ui import ReferenceGalleryInterface

class FatalisManagerMaya(fatalis_manager_main.FatalisManagerMain):
    """
    Maya version of the Fatalis Project Manager UI.
    Should allow you to access to the asset Manager, shot manager and reference inside maya.
    """

    def add_navigations_interface(self):
        self.navigationInterface.addSeparator()
        self.asset_manager_interface = AssetManagerInterfaceMaya(self)
        self.addSubInterface(self.asset_manager_interface, text='Asset Manager', icon=qfluentwidgets.FluentIcon.FOLDER)

        self.shot_manager_interface = ShotManagerInterfaceMaya(self)
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

if __name__ == '__main__':
    """
    loading the UI when calling the file.
    """
    app = QtWidgets.QApplication(sys.argv)
    w = FatalisManagerMaya()
    w.show()
    app.exec()