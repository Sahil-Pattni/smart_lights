import requests

url = 'http://127.0.0.1:5000/'


def post(endpoint, json):
    requests.post(f'{url}{endpoint}', json)