import datetime
import requests
from typing import Any
from pydantic import BaseModel



UPBIT_API_URL = "https://api.upbit.com/v1"
KOBIT_API_URL = "https://api.korbit.co.kr/v1"
BITHUM_API_URL = "https://api.bithumb.com/public"
COINONE_API_URL = "https://api.coinone.co.kr/public/v2"


# UTC 시간을 Unix 시간 (ms)으로 변환하는 함수
def utc_to_unix_ms(utc_datetime: str) -> int:
    return int(utc_datetime.timestamp() * 1000)


def making_time() -> list:
    # 현재 시간 구하기
    now = datetime.datetime.now()

    # 목표 날짜 구하기
    # 현재 시간으로부터 200일씩 뒤로 가면서 datetime 객체 생성하기
    target_date = datetime.datetime(2013, 12, 27, 0, 0, 0)
    result = []
    while now >= target_date:
        result.append(now)
        now -= datetime.timedelta(days=200)
    return result

def header_to_json(url: str) -> Any:
    headers: dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    return response

"""
<<<<<< Market Coin Listing DataFormatting >>>>>>
"""

# coin classification data formatting

class MarketDepend(BaseModel):
    upbit: bool
    bithum: bool
    korbit: bool


class CoinSymbol(BaseModel):
    coin_symbol: str


class DataFormat(CoinSymbol):
    market_depend: MarketDepend


def coin_classification(up: list[str], bit: list[str], kor: list[str], target: str) -> list[dict[str, str]]:
    market_depend = MarketDepend(
        upbit=(target in up),
        bithum=(target in bit),
        korbit=(target in kor)
    )
    return [DataFormat(coin_symbol=target, market_depend=market_depend).model_dump()]