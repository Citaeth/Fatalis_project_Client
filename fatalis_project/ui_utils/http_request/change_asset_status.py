import requests

def change_asset_status(asset_id, new_status):
    url = 'https://fatalisproject.duckdns.org/db_change_asset_status/update_asset_status'
    data = {'asset_id': asset_id, 'status': new_status}

    try:
        response = requests.put(url, json=data)

        if response.status_code == 201:
            print("Asset Status changed successfully!")
        else:
            print("Error:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
