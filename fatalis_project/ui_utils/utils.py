import os
from pathlib import Path
import qfluentwidgets
import xml.etree.ElementTree as ET
import fatalis_project
from fatalis_project.ui_utils.http_request.add_user import add_user_to_database
import zipfile
import tempfile



def get_user_config_file():
    """
    Get the user_config file, located in the fatalis_project.
    Should return the hard path, the root and tree instance to manipulate the whole config.
    Handles both regular execution and PyInstaller execution.
    :return root: config root instance, used to read the data from the config.
    :return tree: config tree instance, used to write the changes.
    :return config_path: file config hard path, used to save it after writing using config_tree.
    """
    config_path = get_user_config_file_path()
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found")

    tree = ET.parse(config_path)
    root = tree.getroot()
    return root, tree, config_path

def get_user_config_file_path():
    """
    Get the user_config file path, located in the fatalis_project.
    Should only return the hard path.
    :return config_path: file config hard path, used to save it after writing using config_tree.
    """
    base_path = Path(fatalis_project.__file__).parent
    config_path = base_path / "user_config.xml"
    return config_path

def get_project_users_config_file():
    """
    Get the user_config file, located in the fatalis_project.
    Should return the hard path, the root and tree instance to manipulate the whole config.
    Handles both regular execution and PyInstaller execution.
    :return root: config root instance, used to read the data from the config.
    :return config_path: file config hard path, used to save it after writing using config_tree.
    """
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
        self.yesButton.setDefault(True)
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
    """
    convert the group of file to send to server into a single zip file.
    :param list files: list of path of the files that we want to send.
    :return:
    """
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