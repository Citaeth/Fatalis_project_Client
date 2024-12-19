import requests

def upload_to_server(file_path, asset_version_name, asset_name, asset_task, asset_status, user_name, infos):
    server_url = "https://fatalisproject.duckdns.org/upload_file/upload"
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            datas = {
                'asset_version_name': asset_version_name,
                'asset_name': asset_name,
                'task': asset_task,
                'status':asset_status,
                'user_name': user_name,
                'infos': infos
            }
            response = requests.post(server_url, files=files, data=datas)
            return response.text
    except Exception as e:
        return "Upload Error: {}".format(e)
