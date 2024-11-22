import fatalis_project
import xml.etree.ElementTree as ET


def get_user_config_file():
    """

    :return:
    """
    file_path = r"C:\Users\Clement\PycharmProjects\Fatalis_Project\fatalis_project\config.xml".format(
        fatalis_project)
    tree = ET.parse(file_path)
    root = tree.getroot()

    return root