import os
from PySide6 import QtWidgets
import xml.etree.ElementTree as ET
import fatalis_project


def get_user_config_file():
    """

    :return:
    """
    fatalis_project_path = os.path.abspath(fatalis_project.__file__).replace("__init__.py", "")
    config_path = "{}user_config.xml".format(fatalis_project_path)
    tree = ET.parse(config_path)
    root = tree.getroot()
    return root


class AddUserName(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("What's your name, Darling?")
        self.setGeometry(100, 100, 300, 150)

        self.label = QtWidgets.QLabel("Enter your name :", self)
        self.input_name = QtWidgets.QLineEdit(self)
        self.bouton = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self
        )

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_name)
        layout.addWidget(self.bouton)
        self.setLayout(layout)

        # Connexions
        self.bouton.accepted.connect(self.accept)
        self.bouton.rejected.connect(self.reject)

    def get_name(self):
        add_name_to_user_config(self.input_name.text())
        return self.input_name.text()


def add_name_to_user_config(name):
    fatalis_project_path = os.path.abspath(fatalis_project.__file__).replace("__init__.py", "")
    config_path = "{}user_config.xml".format(fatalis_project_path)
    tree = ET.parse(config_path)
    root = tree.getroot()
    name_element = root.find("./user/name")
    if name_element.text is None:
        name_element.text = name
    tree.write(config_path, encoding="utf-8", xml_declaration=True)
