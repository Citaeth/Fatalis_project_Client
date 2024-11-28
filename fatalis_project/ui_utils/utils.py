import os
from PySide6 import QtWidgets
import xml.etree.ElementTree as ET
import fatalis_project
from fatalis_project.ui_utils.http_request.add_user import add_user_to_database
import zipfile
import tempfile

def get_user_config_file():
    """
    get the user config file, located in the fatalis_project.
    :return root:
    """
    fatalis_project_path = os.path.abspath(fatalis_project.__file__).replace("__init__.py", "")
    config_path = "{}user_config.xml".format(fatalis_project_path)
    tree = ET.parse(config_path)
    root = tree.getroot()
    return root

def get_project_users_config_file():
    fatalis_project_path = os.path.abspath(fatalis_project.__file__).replace("__init__.py", "")
    config_path = "{}users.xml".format(fatalis_project_path)
    tree = ET.parse(config_path)
    root = tree.getroot()
    return config_path, root

class AddUserName(QtWidgets.QDialog):
    """
    QDialog to ask the user its name, if it's not already fill in the user_config.xml.
    """
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

    def add_name_to_user_config(self):
        """
        normalize the name of the user, and add it to the user_config.xml.
        :return str: name of the user
        """
        user_name_normalize = (self.input_name.text()).replace(" ", "")
        fatalis_project_path = os.path.abspath(fatalis_project.__file__).replace("__init__.py", "")
        config_path = "{}user_config.xml".format(fatalis_project_path)
        tree = ET.parse(config_path)
        root = tree.getroot()
        name_element = root.find("./user/name")
        if name_element.text is None:
            name_element.text = user_name_normalize
        tree.write(config_path, encoding="utf-8", xml_declaration=True)

        add_user_to_database(user_name_normalize)

        return user_name_normalize


def convert_files_group_to_zip(files):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
            zip_path = temp_zip.name
            with zipfile.ZipFile(temp_zip, 'w') as zipf:
                for file_path in files:
                    if os.path.isfile(file_path):
                        zipf.write(file_path, os.path.basename(file_path))
            temp_zip.close()
        return zip_path
    except Exception as e:
        return "Convert to zip error: {}".format(e)