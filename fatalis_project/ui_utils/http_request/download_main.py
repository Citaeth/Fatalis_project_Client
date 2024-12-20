import os
import zipfile
import requests

def download_from_server(asset_id, download_path):
    """
    request to download asset from server, giving its asset_id to find it in the server,
    and the downloading path, where we want to download the asset in local.
    :param str asset_id:
    :param str download_path:
    :return:
    """
    file_path_url = "https://fatalisproject.duckdns.org/download_file/get_file?asset_id={}".format(asset_id)
    try:
        response = requests.get(file_path_url, stream=True)
        if response.status_code == 200:
            zip_file_name = f"asset_{asset_id}.zip"
            zip_save_path = os.path.join(download_path, zip_file_name)
            os.makedirs(download_path, exist_ok=True)
            with open(zip_save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            extract_path = os.path.join(download_path, f"asset_{asset_id}")
            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(zip_save_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            os.remove(zip_save_path)
        else:
            return f"Error retrieving file path: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
