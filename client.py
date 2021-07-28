import requests

data = {'ticker': 'ADAUSDT', 'light': '192.168.1.104'}
url = 'http://127.0.0.1:5000/stonks'

requests.post(url, json=data)