import requests
from pydantic import BaseModel

from pathlib import Path
from typing import Any


UPBIT_API_URL = "https://api.upbit.com/v1"
KOBIT_API_URL = "https://api.korbit.co.kr/v1"
BITHUM_API_URL = "https://api.bithumb.com/public"
PRESENT_DIR: Path = Path(__file__).resolve().parent


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
    listup = []

    market_depend = MarketDepend(
        upbit=(target in up),
        bithum=(target in bit),
        korbit=(target in kor)
    )

    listup.append(
        DataFormat(
            coin_symbol=target,
            market_depend=market_depend
        ).model_dump()
    )

    return listup