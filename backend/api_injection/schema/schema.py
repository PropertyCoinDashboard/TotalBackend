import requests
from typing import Optional, Any 



"""
스키마 모음 집  
"""


def header_to_json(url: str):
    headers: dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info


# CSV -> JSON 변환 
def csv_read_json(read_data: str) -> list[dict[str, Any]]:
    import csv

    with open(read_data, "r") as cj:
        csv_data = csv.DictReader(cj)
        data = list(csv_data)

    return data


def data_format(coin_symbol: str, korean_name: str, 
                up: bool, bit: bool, kor: bool) -> dict[str, dict[str, bool]]:
    data: dict = {
        "coin_symbol": coin_symbol,
        "korean_name": korean_name,
        "market_depend": {
                "upbit": up, 
                "bithum": bit,
                "korbit": kor,
            }
    }
    return data


# 개극혐 너무 불편 쌉불편 바꾸고싶음 소름돋음 
def coin_classification(up = None, bit = None, kor = None,
                        target: Optional[str] = None, 
                        korean_name: Optional[str] = None) -> list[dict[str, str]]:
    listup: list = []
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
