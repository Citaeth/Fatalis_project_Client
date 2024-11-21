from PySide6 import QtWidgets
import qfluentwidgets


class SingleDirectionScrollInterface(qfluentwidgets.SingleDirectionScrollArea):
    """
    The Asset Manager Interface is a Widget who contain the Shot Manager.
    Should be called in the Fatalis Project main UI. It could be bypassed in the Shot Manager in the software, calling
    directly the ShotManagerApplication.
    """
    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.view = QtWidgets.QWidget(self)
        self.vBoxLayout = QtWidgets.QVBoxLayout(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName('Generic Interface')

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 15, 0)

        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')
