import requests
import pandas as pd 
import threading
from typing import Dict, Final, Any, List
from kafka import KafkaProducer


UPBIT_API_URL: Final[str] = "https://api.upbit.com/v1"
BITHUM_API_URL: Final[str] = "https://api.bithumb.com/public/ticker"
"""
업비트 토큰 가격 업데이트 주기 카프카 맞추기
"""


def header_to_json(url: str):
    headers: Dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info

def data_format(name, open, high, low, present) -> Dict:
    data = {
        "market_name": name,
        "open": open,
        "high": high,
        "low": low,
        "present": present
    }
    return data


# 프로세스 나누기 
class UpBitAPIGeneration:
    def __init__(self) -> None:
        self.up_url = UPBIT_API_URL
    
    def upbit_coin_total_market_json(self) -> List[Dict[str, str]]:
        url: str = f"{self.up_url}/market/all?isDetails=true"
        return header_to_json(url)

    def upbit_coin_price_json(self) -> List[Dict[str, str]]:
        url: str = f"{self.up_url}/candles/minutes/1?market=KRW-BTC&count=1"
        return header_to_json(url)
    
    def upbit_bitcoin_present_price(self) -> pd.DataFrame:
        url: str = f'{self.up_url}/ticker?markets=KRW-BTC'
        data = header_to_json(url)
        for i in data:
            up_bitcoin_pd = data_format(
                name    = "upbit-BTC",
                open    = i["opening_price"],
                high    = i["high_price"],
                low     = i["low_price"],
                present = i["trade_price"]
            )
        return pd.DataFrame(up_bitcoin_pd, index=[0])
    

class BithumAPIGeneration:
    def __init__(self) -> None:
        self.bit_url = BITHUM_API_URL

    def bithum_coin_total_market_json(self) -> List[str]:
        url: str = f"{self.bit_url}/ALL_KRW"
        data: Dict[Any, Any] = header_to_json(url)

        return [i for i in data["data"]]
    
    def bithum_bitcoin_present_price(self) -> pd.DataFrame:
        url: str = f"{self.bit_url}/BTC_KRW"
        data: Dict[str] = header_to_json(url)
        bbitcoin_pd = data_format(
            name    = "bithum-BTC",
            open    = data["data"]["opening_price"],
            high    = data["data"]["max_price"],
            low     = data["data"]["min_price"],
            present = data["data"]["closing_price"]
        )
        return pd.DataFrame(bbitcoin_pd, index=[0])



def concatnate() -> pd.DataFrame:
    bit = BithumAPIGeneration().bithum_bitcoin_present_price()
    upbit = UpBitAPIGeneration().upbit_bitcoin_present_price()
    
    concat_data_bit = pd.concat([bit, upbit])

    return concat_data_bit
    

import time
while True:
    time.sleep(1)
    print(concatnate())