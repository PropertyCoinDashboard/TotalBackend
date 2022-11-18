import requests
from typing import Dict, Final, Any, List
from kafka import KafkaProducer


UPBIT_API_URL: Final[str] = "https://api.upbit.com/v1"
BITHUM_API_URL: Final[str] = "https://api.bithumb.com/public/ticker"
"""
업비트 토큰 가격 업데이트 주기 카프카 맞추기
"""

# 프로세스 나누기 
class UpBitAPIGeneration:
    pass


class BithumAPIGeneration:
    pass


class CobitAPIGeneration:
    pass


class CoinoneAPIGeneration:
    pass



def header_to_json(url: str) -> List[Dict[Any, Any]]:
    headers: Dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info


def bithum_coin_total_market_json() -> List[str]:
    url: str = f"{BITHUM_API_URL}/ALL_KRW"
    data: List[Dict[Any, Any]] = header_to_json(url)

    return [i for i in data["data"]]


def upbit_coin_total_market_json() -> List[Dict[str, str]]:
    url: str = f"{UPBIT_API_URL}/market/all?isDetails=true"

    return header_to_json(url)


def up_bit_coin_price_json() -> List[Dict[str, str]]:
    url: str = f"{UPBIT_API_URL}/candles/minutes/1?market=KRW-BTC&count=1"

    return header_to_json(url)



print(bithum_coin_total_market_json())