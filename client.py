import requests

url = 'http://192.168.1.103:5000/'
data = { 'ticker': 'ADAUSDT', 'light': '192.168.1.104', 'delay': 1.2}

def post(endpoint, data:dict):
    requests.post(f'{url}{endpoint}', json=data)