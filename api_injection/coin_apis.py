import sys
import requests
from typing import Dict, Final, Any, List, Tuple


UPBIT_API_URL: Final[str] = "https://api.upbit.com/v1"
BITHUM_API_URL: Final[str] = "https://api.bithumb.com/public/ticker"


def header_to_json(url: str):
    headers: Dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info


class CoinMarketBitCoinPresentPrice:
    def __init__(self) -> None:
        self.upbit_bitcoin_present_price = header_to_json(f"{UPBIT_API_URL}/ticker?markets=KRW-BTC")[0]
        self.bithum_bitcoin_present_price = header_to_json(f"{BITHUM_API_URL}/BTC_KRW")["data"]
           
               
class UpbitAPIBitcoin:
    def __init__(self) -> None:
        self.up_url = UPBIT_API_URL
        self.upbit_market = header_to_json(f"{self.up_url}/market/all?isDetails=true")
        self.upbit_coin_present_price = header_to_json(f'{self.up_url}/ticker?markets=KRW-BTC')     

    def __getitem__(self, index: int) -> Dict:
        return self.upbit_coin_present_price[index]
    
    def __sizeof__(self) -> int:
        return sys.getsizeof(self.upbit_coin_present_price)   
    
    
class BithumAPIBitcoin:
    def __init__(self) -> None:
        self.bit_url = BITHUM_API_URL
        self.bithum_market = header_to_json(f"{self.bit_url}/ALL_KRW")
        self.bithum_present_price = header_to_json(f"{self.bit_url}/BTC_KRW")

    def bithum_market_list(self) -> List[str]:    
        return [coin for coin in self.bithum_market["data"]]
        
    def __index__(self, index: int) -> str:
        return self.bithum_market_list[index]

    def __getitem__(self, index: str) -> Dict:
        return self.bithum_present_price[index]
    
    def __sizeof__(self) -> int:
        return sys.getsizeof(self.bithum_present_price)
    
    def __namesplit__(self, index) -> str:
        return f"{self.bit_url}/BTC_KRW".split("/")[index]