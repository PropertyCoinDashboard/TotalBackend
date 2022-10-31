import requests


def upbit_coin_total_market_json():
    url = "https://api.upbit.com/v1/market/all?isDetails=false"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info
