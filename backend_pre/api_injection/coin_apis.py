import sys
from pathlib import Path

# 현재 파일의 경로
file_path = Path(__file__).resolve()
# 상위 경로 backend
parent_path = file_path.parent

# 상위 경로 backed_pre -> sys 경로 추가
grandparent_path = parent_path.parent
backend__ = f"{str(grandparent_path)}/backend/backend_pre/api_injection/schema"
sys.path.append(str(parent_path))
sys.path.append(str(grandparent_path))
sys.path.append(backend__)


from pathlib import Path
from typing import (
    Any, Optional, Literal, Dict, List, Generator
)
from api_util import (
    header_to_json, coin_classification, csv_read_json
)


UPBIT_API_URL: Literal = "https://api.upbit.com/v1"
KOBIT_API_URL: Literal = "https://api.korbit.co.kr/v1"
BITHUM_API_URL: Literal = "https://api.bithumb.com/public"
PRESENT_DIR: Path = Path(__file__).resolve().parent


# # 비트코인 현재가
# class CoinMarketBitCoinPresentPrice:
#     def __init__(self) -> None:
#         self.upbit_bitcoin_present_price = header_to_json(f"{UPBIT_API_URL}/ticker?markets=KRW-BTC")[0]
#         self.bithum_bitcoin_present_price = header_to_json(f"{BITHUM_API_URL}/ticker/BTC_KRW")["data"]
#         self.korbit_bitcoin_present_price = header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair=btc_krw")


# # 이더리움 현재가 
# class CoinMarketEthereumPresentPrice:
#     def __init__(self) -> None:
#         self.upbit_ethereum_present_price = header_to_json(f"{UPBIT_API_URL}/ticker?markets=KRW-ETH")[0]
#         self.bithum_ethereum_present_price = header_to_json(f"{BITHUM_API_URL}/ticker/ETH_KRW")["data"]
#         self.korbit_ethereum_present_price = header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair=eth_krw")


class ApiBasicArchitecture:     
    def __init__(self, name: Optional[str] = None) -> None:
        self.name: str = name 
        self.upbit_market = header_to_json(f"{UPBIT_API_URL}/market/all?isDetails=true")
        self.bithum_market = header_to_json(f"{BITHUM_API_URL}/ticker/ALL_KRW")
        self.korbit_market = header_to_json(f"{KOBIT_API_URL}/ticker/detailed/all")
        
    def __namesplit__(self) -> str:
        return self.name.upper()


class UpbitAPI(ApiBasicArchitecture):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)        
        # 현재가 
        self.upbit_present_url_parameter: str = f'ticker?markets=KRW-{self.name}'
        self.upbit_coin_present_price = header_to_json(f'{UPBIT_API_URL}/{self.upbit_present_url_parameter}')   
        
    def upbit_market_list(self) -> List[str]:
        return [i["market"].split("-")[1] for i in self.upbit_market if i["market"].startswith("KRW-")]
    
    def upbit_market_keyvalue(self) -> List[Dict[str, str]]:        
        return [{"korean_name": i["korean_name"], "coin_symbol": i["market"].split("-")[1]} 
                 for i in self.upbit_market if i["market"].startswith("KRW-")]
                
    def __getitem__(self, index: int) -> Dict:
        return self.upbit_coin_present_price[index] 
    

class BithumAPI(ApiBasicArchitecture):
    data: str = f"{PRESENT_DIR}/data/bithum.csv"

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.bithum_present_price = header_to_json(f"{BITHUM_API_URL}/ticker/{self.name}_KRW")
        
    def bithum_market_list(self) -> List:
        a = [coin for coin in self.bithum_market["data"]]
        del a[-1]
        return a
    
    def bithum_market_keyvalue(self) -> List[Dict[str, Any]]:      
        return csv_read_json(self.data)
             
    def __getitem__(self, index: str) -> Any:
        return self.bithum_present_price[index]
    

class KorbitAPI(ApiBasicArchitecture):
    data: str = f"{PRESENT_DIR}/data/korbit.csv"

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.korbit_present_price: str = f"{KOBIT_API_URL}/ticker/detailed?currency_pair"

    def korbit_market_list(self) -> List:
        return [i.split("_")[0].upper() for i in self.korbit_market]
    
    def korbit_market_keyvalue(self) -> List[Dict[str, Any]]:        
        return csv_read_json(self.data)

    def __getitem__(self, index: str) -> Any:
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
    
    def coin_key_value_concat(self) -> Generator[Dict[str, str], Any, Any]:
        up = self.upbit_market_keyvalue()
        bit = self.bithum_market_keyvalue()
        kor = self.korbit_market_keyvalue()
        total: List = up + bit + kor
        a = ({v['coin_symbol']:v for v in total}.values())
        return a
    
    def coin_total_dict(self) -> List[Dict[str, str]]:
        up = self.upbit_market_list()
        bit = self.bithum_market_list()
        kor = self.korbit_market_list()
        coin_info = self.coin_key_value_concat()

        coin_info_generator: Generator[List[Dict[str, str]]] = (
            coin_classification(up=up, bit=bit, kor=kor, 
                                target=name["coin_symbol"], korean_name=name["korean_name"]) 
                                for name in coin_info)
        result: List[Dict[str, str]] = [data for i in coin_info_generator for data in i]
        
        return result

