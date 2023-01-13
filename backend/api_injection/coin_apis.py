import sys
import requests
from typing import Final, Any, Optional


UPBIT_API_URL: Final[str] = "https://api.upbit.com/v1"
KOBIT_API_URL: Final[str] = "https://api.korbit.co.kr/v1"
BITHUM_API_URL: Final[str] = "https://api.bithumb.com/public/ticker"


def header_to_json(url: str):
    headers: dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info


def dict_organizer(target) -> dict:
    d: dict = {}
    for data in target:
        if data in d: # 이미 등장한 값의 경우
            d[data] += 1
        else: # 처음 등장한 값의 경우
            d[data] = 1        
    return d


class CoinMarketBitCoinPresentPrice:
    def __init__(self) -> None:
        self.upbit_bitcoin_present_price = header_to_json(f"{UPBIT_API_URL}/ticker?markets=KRW-BTC")[0]
        self.korbit_bitcoin_present_price = header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair=btc_krw")
        self.bithum_bitcoin_present_price = header_to_json(f"{BITHUM_API_URL}/BTC_KRW")["data"]
        

class UpbitAPI:
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__()
        self.name = name
        self.up_url = UPBIT_API_URL
        self.upbit_market = header_to_json(f"{self.up_url}/market/all?isDetails=true")
        self.upbit_present_url_parameter = f'ticker?markets=KRW-{self.name}'
        self.upbit_coin_present_price = header_to_json(f'{self.up_url}/{self.upbit_present_url_parameter}')     

    def upbit_market_list(self) -> list[str]:
        return [data["market"].split("-")[1] for data in self.upbit_market]

    def __getitem__(self, index: int) -> dict:
        return self.upbit_coin_present_price[index]
     
    def __sizeof__(self) -> int:
        return sys.getsizeof(self.upbit_coin_present_price)   
    
    def __namesplit__(self) -> str:
        return self.name.upper()
    

class BithumAPI:
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__()
        self.name = name
        self.bit_url = BITHUM_API_URL
        self.bithum_market = header_to_json(f"{self.bit_url}/ALL_KRW")
        self.bithum_present_price = header_to_json(f"{self.bit_url}/{name}_KRW")

    def bithum_market_list(self) -> list[Any]:
        a = [coin for coin in self.bithum_market["data"]]
        del a[-1]
        return a
        
    def __getitem__(self, index: str) -> dict:
        return self.bithum_present_price[index]
    
    def __sizeof__(self) -> int:
        return sys.getsizeof(self.bithum_present_price)
    
    def __namesplit__(self) -> str:
        return self.name.upper()


class KorbitAPI:
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__()
        self.name = name 
        self.url = KOBIT_API_URL
        self.korbit_market = header_to_json(f"{self.url}/ticker/detailed/all")
        self.korbit_present_price = f"{self.url}/ticker/detailed?currency_pair"

    def korbit_market_list(self) -> list[str]:
        return [i.strip("_krw").upper() for i in self.korbit_market]

    def __getitem__(self, index: str) -> dict:
        return header_to_json(f"{self.korbit_present_price}={index.lower()}_krw")
    
    def __namesplit__(self) -> str:
        return self.name.upper()
    
    
class TotalCoinMarketlistConcatnate(UpbitAPI, BithumAPI, KorbitAPI):
    def __init__(self) -> None:
        super().__init__()
    
    def coin_total_preprecessing(self) -> dict:
        """
        모든 거래소 코인 목록 통합 
        """
        up = self.upbit_market_list()
        bit = self.bithum_market_list()     
        kor = self.korbit_market_list()   
        
        total: list = up + bit + kor
        return dict_organizer(target=total)
        
    def coin_total_list(self) -> list:
        return [name for name, index in self.coin_total_preprecessing().items() if index >= 2]
        
