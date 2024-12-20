import requests

def add_user_to_database(user_name):
    """
    request to add the username register in the UI by a new user, into the server database.
    :param str user_name:
    :return:
    """
    url = 'https://fatalisproject.duckdns.org/db_add_user/add_user'
    data = {'username': user_name}

    try:
        response = requests.post(url, json=data)

        if response.status_code == 201:
            print("User added successfully!")
        else:
            print("Error:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
