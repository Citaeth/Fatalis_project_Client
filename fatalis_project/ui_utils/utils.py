import os
from pathlib import Path
from PySide6 import QtWidgets, QtGui, QtCore
import xml.etree.ElementTree as ET
import fatalis_project
from fatalis_project.ui_utils.http_request.add_user import add_user_to_database
import zipfile
import tempfile

import qfluentwidgets


def get_user_config_file():
    """
    Get the user config file, located in the fatalis_project.
    Handles both regular execution and PyInstaller execution.
    :return root:
    """
    config_path = get_user_config_file_path()
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found")

    tree = ET.parse(config_path)
    root = tree.getroot()
    return root, tree, config_path

def get_user_config_file_path():
    base_path = Path(fatalis_project.__file__).parent
    config_path = base_path / "user_config.xml"
    return config_path

def get_project_users_config_file():
    base_path = Path(fatalis_project.__file__).parent
    config_path = base_path / "users.xml"

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found")

    tree = ET.parse(config_path)
    root = tree.getroot()
    return config_path, root

class AddUserName(qfluentwidgets.Dialog):
    """
    QDialog to ask the user its name, if it's not already fill in the user_config.xml.
    """
    def __init__(self):
        super().__init__("What's your name, Darling?", 'Enter your name :')
        self.setTitleBarVisible(False)
        layout = self.layout()
        self.input_name = qfluentwidgets.LineEdit(self)
        layout.addChildWidget(self.input_name)
        self.input_name.move(150, 60)

        self.setLayout(layout)


    def add_name_to_user_config(self):
        """
        normalize the name of the user, and add it to the user_config.xml.
        :return str: name of the user
        """
        user_name_normalize = (self.input_name.text()).replace(" ", "")
        config_path = get_user_config_file_path()
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