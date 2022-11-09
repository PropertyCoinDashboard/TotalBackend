import requests
from kafka import KafkaProducer


UPBIT_API_URL = "https://api.upbit.com/v1"


def header_to_json(url):
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    return info


def upbit_coin_total_market_json():
    url = f"{UPBIT_API_URL}/market/all?isDetails=true"
    return header_to_json(url)
    

def up_bit_coin_price_json():
    url = f"{UPBIT_API_URL}/candles/minutes/1?market=KRW-BTC&count=1"

    return header_to_json(url)


