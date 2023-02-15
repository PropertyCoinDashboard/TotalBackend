import csv
import requests
from typing import Any 



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


def coin_classification(up: list = None, bit: list = None, kor: list = None,
                        target: str = None, 
                        korean_name: str = None) -> list[dict[str, str]]:
    listup: list = []
    for exchange in ['up', 'bit', 'kor']:
        if target in locals()[exchange]:
            up_value, bit_value, kor_value = (exchange == 'up', exchange == 'bit', exchange == 'kor')
            listup.append(data_format(coin_symbol=target, korean_name=korean_name, 
                                      up=up_value, bit=bit_value, kor=kor_value))
            break
    return listup

