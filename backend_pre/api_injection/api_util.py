import csv
import requests
from pathlib import Path
from typing import (
    Any, Literal, Dict, List
)

UPBIT_API_URL: Literal = "https://api.upbit.com/v1"
KOBIT_API_URL: Literal = "https://api.korbit.co.kr/v1"
BITHUM_API_URL: Literal = "https://api.bithumb.com/public"
PRESENT_DIR: Path = Path(__file__).resolve().parent


def header_to_json(url: str) -> Any:
    headers: Dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info


# CSV -> JSON 변환 
def csv_read_json(read_data: str) -> List[Dict[str, Any]]:
    with open(read_data, "r") as cj:
        csv_data = csv.DictReader(cj)
        data = list(csv_data)

    return data


def data_format(coin_symbol: str, korean_name: str, 
                up: bool, bit: bool, kor: bool) -> Dict[str, Dict[str, bool]]:
    data: Dict = {
        "coin_symbol": coin_symbol,
        "korean_name": korean_name,
        "market_depend": {
                "upbit": up, 
                "bithum": bit,
                "korbit": kor,
            }
    }
    return data

    
def coin_classification(up: List = None, bit: List = None, kor: List = None,
                        target: str = None, korean_name: str = None) -> list:
    listup: List = []
    if (target in up) and (target in bit) and (target in kor):
        listup.append(data_format(coin_symbol=target, korean_name=korean_name, up=True, bit=True, kor=True))
    elif (target in up) and (target in bit):
        listup.append(data_format(coin_symbol=target, korean_name=korean_name, up=True, bit=True, kor=False))
    elif (target in up) and (target in kor):
        listup.append(data_format(coin_symbol=target, korean_name=korean_name, up=True, bit=False, kor=True))
    elif (target in bit) and (target in kor):
        listup.append(data_format(coin_symbol=target, korean_name=korean_name, up=False, bit=True, kor=True))
    elif target in up:
        listup.append(data_format(coin_symbol=target, korean_name=korean_name, up=True, bit=False, kor=False))
    elif target in bit:
        listup.append(data_format(coin_symbol=target, korean_name=korean_name, up=False, bit=True, kor=False))
    elif target in kor:
        listup.append(data_format(coin_symbol=target, korean_name=korean_name, up=False, bit=False, kor=True))

    return listup