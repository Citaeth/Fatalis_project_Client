import requests

def get_assets_from_database():
    """
    Request HTTPS to get the assets database information. The Goal is to use this table information to fill the main
    table of the manager.
    :return:
    """
    url = 'https://fatalisproject.duckdns.org/db_get_assets/get_assets'

    try:
        # Envoi de la requête GET
        response = requests.get(url)

        # Vérification du code de statut HTTP
        if response.status_code == 200:
            # Récupération des données JSON
            data = response.json()
            if 'assets' in data:
                # Affichage des colonnes
                print(f"Columns: {', '.join(data['assets']['columns'])}")
                print("Data:")
                # Affichage des lignes
                for row in data['assets']['data']:
                    print(row)
            else:
                print("No data found.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

get_assets_from_database()

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
                print(f"Columns: {', '.join(data['files']['columns'])}")
                print("Data:")
                for row in data['files']['data']:
                    print(row)
            else:
                print("No data found.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


get_files_from_database()
