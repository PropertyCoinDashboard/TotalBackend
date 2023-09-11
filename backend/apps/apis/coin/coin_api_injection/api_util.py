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
    bithum: bool
    korbit: bool


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


def coin_classification(
    up: List[str] = None,
    bit: List[str] = None,
    kor: List[str] = None,
    target: Optional[str] = None,
    korean_name: Optional[str] = None,
) -> List[Dict[str, str]]:
    listup: List[DataFormat] = []
    market_depend = MarketDepend(
        upbit=(target in up), bithum=(target in bit), korbit=(target in kor)
    )

    listup.append(
        asdict(
            DataFormat(
                coin_symbol=target, korean_name=korean_name, market_depend=market_depend
            )
        )
    )

    return listup
