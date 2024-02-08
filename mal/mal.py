import requests
import json
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s:%(message)s")

BASE_URL = 'https://api.myanimelist.net/v2'

TOKEN_FILE = "/home/battos/Projects/AniReco/mal/token.json"

def get_token():
    with open(TOKEN_FILE) as file:
        data = json.loads(file.read())
    return data.get('access_token', None)


TOKEN = get_token()

def get_mal(url: str,
            access_token: str,
            params: Dict = None,
            extra_headers: Dict = {}):
    headers = {
        'Authorization': f'Bearer {access_token}',
        **extra_headers,
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    response.close()
    return data