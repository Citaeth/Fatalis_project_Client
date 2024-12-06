import requests
import xml.etree.ElementTree as ET
from fatalis_project.ui_utils import utils

def get_assets_from_database():
    """
    Request HTTPS to get the assets database information. The Goal is to use this table information to fill the main
    table of the manager.
    :return:
    """
    url = 'https://fatalisproject.duckdns.org/db_get_assets/get_assets'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'assets' in data:
                assets_dict = data['assets']['data']
                return assets_dict
            else:
                return "No data found."
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def get_files_from_database():
    """
    Request HTTPS to get the files database information. The Goal is to use this table information to know where the
    selected asset is to download it without look at all the server content.
    The files table should have an 'asset id' column, to make a faster link with the selected asset.
    :return:
    """
    url = 'https://fatalisproject.duckdns.org/db_get_files/get_files'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'files' in data:
                files_dict = data['files']['data']
                return files_dict
            else:
                return"No data found."
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def fetch_users_from_db():
    """Connect to the remote PostgreSQL database and fetch all users."""
    url = 'https://fatalisproject.duckdns.org/db_get_users/get_users'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'users' in data:
                user_dict = data['users']['data']
                for user in user_dict:
                    user.pop('created_at', None)
                return user_dict
            else:
                return "No data found."
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def save_to_xml(users, xml_file):
    """Save users data to an XML file."""
    root = ET.Element("Users")

    for user in users:
        user_element = ET.SubElement(root, "User")

        ET.SubElement(user_element, "ID").text = str(user['id'])
        ET.SubElement(user_element, "Username").text = user['username']

    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)


def load_from_xml(xml_file):
    """Load users data from an XML file."""
    try:
        users = []
        for user_element in xml_file.findall("User"):
            user = {}
            user_id = int(user_element.find("ID").text)
            username = user_element.find("Username").text
            user['id'] = user_id
            user['username'] = username
            users.append(user)
        return users
    except Exception as e:
        print(f"Error reading XML: {e}")
        return []


def compare_and_update_db():
    """Compare DB and XML, and update XML if necessary."""
    user_xml_path, users_xml_root = utils.get_project_users_config_file()
    users_from_db = fetch_users_from_db()
    users_from_xml = load_from_xml(users_xml_root)
    if users_from_db != users_from_xml:
        print("Updating XML file...")
        save_to_xml(users_from_db, user_xml_path)
    else:
        print("XML file is up-to-date.")