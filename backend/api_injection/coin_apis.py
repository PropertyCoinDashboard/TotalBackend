import requests
from collections import Counter
from typing import Final, Any, Optional, Generator


UPBIT_API_URL: Final[str] = "https://api.upbit.com/v1"
KOBIT_API_URL: Final[str] = "https://api.korbit.co.kr/v1"
BITHUM_API_URL: Final[str] = "https://api.bithumb.com/public"


def header_to_json(url: str):
    headers: dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info


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
                        korean_name: Optional[str] = None) -> None:
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


# CSV -> JSON 변환 
def csv_read_json(read_data: str) -> list[dict[str, Any]]:
    import csv

    with open(read_data, "r") as cj:
        csv_data = csv.DictReader(cj)
        data = list(csv_data)

    return data


class CoinMarketBitCoinPresentPrice:
    def __init__(self) -> None:
        self.upbit_bitcoin_present_price = header_to_json(f"{UPBIT_API_URL}/ticker?markets=KRW-BTC")[0]
        self.korbit_bitcoin_present_price = header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair=btc_krw")
        self.bithum_bitcoin_present_price = header_to_json(f"{BITHUM_API_URL}/BTC_KRW")["data"]


class ApiBasicArchitecture:     
    def __init__(self, name: Optional[str] = None) -> None:
        self.name: str = name 
        
    def __namesplit__(self) -> str:
        return self.name.upper()


class UpbitAPI(ApiBasicArchitecture):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.upbit_market = header_to_json(f"{UPBIT_API_URL}/market/all?isDetails=true")
        
        # 현재가 
        self.upbit_present_url_parameter: str = f'ticker?markets=KRW-{self.name}'
        self.upbit_coin_present_price = header_to_json(f'{UPBIT_API_URL}/{self.upbit_present_url_parameter}')   
        
    def upbit_market_list(self) -> list[str]:
        return [i["market"].split("-")[1] for i in self.upbit_market if i["market"].split("-")[0] == "KRW"]
    
    def upbit_market_keyvalue(self) -> list[dict[str, str]]:        
        return [{"korean_name": i["korean_name"], "coin_symbol": i["market"].split("-")[1]} 
                 for i in self.upbit_market if i["market"].split("-")[0] == "KRW"]
                
    def __getitem__(self, index: int) -> dict:
        return self.upbit_coin_present_price[index] 
    

class BithumAPI(ApiBasicArchitecture):
    data = "data/bithum.csv"
    
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.bit_url: str = BITHUM_API_URL
        self.bithum_market = header_to_json(f"{BITHUM_API_URL}/ticker/ALL_KRW")
        self.bithum_present_price = header_to_json(f"{BITHUM_API_URL}/ticker/{self.name}_KRW")
        
    def bithum_market_list(self) -> list[Any]:
        a = [coin for coin in self.bithum_market["data"]]
        del a[-1]
        return a
    
    def bithum_market_keyvalue(self) -> csv_read_json:      
        return csv_read_json(self.data)
             
    def __getitem__(self, index: str) -> dict:
        return self.bithum_present_price[index]
    

class KorbitAPI(ApiBasicArchitecture):
    data = "data/korbit.csv"
    
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.korbit_market = header_to_json(f"{KOBIT_API_URL}/ticker/detailed/all")
        self.korbit_present_price: str = f"{KOBIT_API_URL}/ticker/detailed?currency_pair"

    def korbit_market_list(self) -> list[str]:
        return [i.split("_")[0].upper() for i in self.korbit_market]
    
    def korbit_market_keyvalue(self) -> csv_read_json:        
        return csv_read_json(self.data)

    def __getitem__(self, index: str) -> dict:
        """
        :param index : str 
            ex) btc eth 
        :return 
            값
        """
        return header_to_json(f"{self.korbit_present_price}={index.lower()}_krw")
    
    
class TotalCoinMarketlistConcatnate(UpbitAPI, BithumAPI, KorbitAPI):
    def __init__(self) -> None:
        super().__init__()
    
    def coin_key_value_concat(self) -> list[dict[str, str]]:
        up = self.upbit_market_keyvalue()
        bit = self.bithum_market_keyvalue()
        kor = self.korbit_market_keyvalue()
        total: list = up + bit + kor
        a = list({v['coin_symbol']:v for v in total}.values())
        return a
    
    # def __coin_mixin(self) -> dict:
    #     """
    #     모든 거래소 코인 목록 통합 
    #     """
    #     up = self.upbit_market_list()
    #     bit = self.bithum_market_list()     
    #     kor = self.korbit_market_list()   
    #     total: list[str] = up + bit + kor
    #     return Counter(total)
    
    # def coin_total_list(self) -> list[str]:
    #     return [name for name, index in self.__coin_mixin().items() if index >= 3]
    
    def coin_total_dict(self):
        up = self.upbit_market_list()
        bit = self.bithum_market_list()
        kor = self.korbit_market_list()
        coin_info = self.coin_key_value_concat()

        a = (coin_classification(up=up, bit=bit, kor=kor,
                                target=name["coin_symbol"], 
                                korean_name=name["korean_name"]) for name in coin_info)
        b = [data for i in a for data in i]
        
        return b
