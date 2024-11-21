import os
from PySide6 import QtWidgets, QtCore, QtGui
import qfluentwidgets

class ReferenceGalleryInterface(qfluentwidgets.SingleDirectionScrollArea):
    """
    The Asset Manager Interface is a Widget who contain the Asset Manager.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QtWidgets.QWidget(self)
        self.vBoxLayout = QtWidgets.QVBoxLayout(self.view)
        self.appAssetManager = ReferenceGalleryApplication(self)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName('References Gallery Interface')

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.appAssetManager)

        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')


class ReferenceGalleryApplication(qfluentwidgets.HeaderCardWidget):
    """ Gallery card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('References Gallery')

        flip_view = qfluentwidgets.VerticalFlipView(self)
        flip_view.addImages(self.get_resources_images())
        flip_view.setSpacing(10)

        flip_view.setAspectRatioMode(QtGui.Qt.AspectRatioMode.KeepAspectRatio)

        self.viewLayout.addWidget(flip_view)


    @staticmethod
    def get_resources_images():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resources_dir = os.path.join(script_dir, 'resources')

        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        images = [
            os.path.join(resources_dir, f)
            for f in os.listdir(resources_dir)
            if os.path.splitext(f)[1].lower() in valid_extensions
        ]

        return images
