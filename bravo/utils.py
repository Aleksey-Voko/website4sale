import requests

from bravo.data import HEADERS


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    print(url)
    print(response.status_code)
    print('=' * 30)
    return response.text
