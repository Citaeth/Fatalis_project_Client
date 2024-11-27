import requests

def upload_to_server(file_path, server_url):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(server_url, files=files)
            return response
    except Exception as e:
        return "Upload Error: {}".format(e)

file_path = r"C:\Users\Clement\Desktop\test_upload.txt"  # Local path of uploaded asset/folder
server_url = "https://fatalisproject.duckdns.org/upload"  # Flask server adress
upload_to_server(file_path, server_url)