import requests
import datetime
import csv

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Literal, Dict, List, Optional


UPBIT_API_URL: Literal = "https://api.upbit.com/v1"
KOBIT_API_URL: Literal = "https://api.korbit.co.kr/v1"
BITHUM_API_URL: Literal = "https://api.bithumb.com/public"
PRESENT_DIR: Path = Path(__file__).resolve().parent


def making_time() -> List:
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
    headers: Dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    return response


# CSV -> JSON 변환 
def csv_read_json(read_data: str) -> list[dict[str, Any]]:
    with open(read_data, "r") as cj:
        csv_data = csv.DictReader(cj)
        data = list(csv_data)

    return data


"""
<<<<<< Market Coin Listing DataFormatting >>>>>>
"""

# coin classification data formatting
@dataclass(frozen=True)
class MarketDepend:
    upbit: bool
    bit: bool
    kor: bool


# market coin symbol 
@dataclass
class CoinSymbol:
    coin_symbol: str


@dataclass
class CoinKoreaNameSymbol(CoinSymbol):
    korean_name: str
        
        
# coin market listing
@dataclass
class DataFormat(CoinKoreaNameSymbol):
    market_depend: Dict[str, bool] = MarketDepend
    
        
def coin_classification(up:  List[str] = None, 
                        bit: List[str] = None, 
                        kor: List[str] = None,
                        target: Optional[str] = None, 
                        korean_name: Optional[str] = None) -> List[DataFormat]:
    
    listup: List[DataFormat] = []
    market_depend = MarketDepend(
        up=(target in up),
        bit=(target in bit),
        kor=(target in kor)
    )
    
    listup.append(asdict(DataFormat(coin_symbol=target, korean_name=korean_name, market_depend=market_depend)))

    return listup