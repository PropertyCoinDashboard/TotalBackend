from pathlib import Path
from abc import ABC, abstractmethod
from typing import (
    Any, 
    Dict, 
    List,
    Optional, 
)

from api_util import CoinSymbol, CoinKoreaNameSymbol
from api_util import (
    UPBIT_API_URL, 
    BITHUM_API_URL, 
    KOBIT_API_URL,
    PRESENT_DIR
)
from api_util import (
    header_to_json, 
    coin_classification, 
    csv_read_json, 
    asdict
)



class ApiBasicArchitecture(ABC):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name: str = name
        
    @abstractmethod
    def market_keyvalue(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def market_list(self) -> List[str]:
        pass

    def __namesplit__(self) -> str:
        return self.name.upper()



class UpbitAPI(ApiBasicArchitecture):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        # 마켓 코인 정보 
        self.upbit_market = header_to_json( f"{UPBIT_API_URL}/market/all?isDetails=true")
        # 코인 현재가 
        self.upbit_coin_present_price = header_to_json(f"{UPBIT_API_URL}/ticker?markets=KRW-{self.name}")
    
    def market_list(self) -> List[str]:
        return [
                CoinSymbol(coin_symbol=coin["market"].split("-")[1]).coin_symbol
                for coin in self.upbit_market 
                if coin["market"].startswith("KRW-")
            ]
        
    def market_keyvalue(self) -> List[Dict[str, Any]]:
        return [
                asdict(CoinKoreaNameSymbol(korean_name=cv["market"].split("-")[1],
                                           coin_symbol=cv["korean_name"]))
                for cv in self.upbit_market 
                if cv["market"].startswith("KRW-")
            ]


class BithumAPI(ApiBasicArchitecture):
    data: str = f"{PRESENT_DIR}/data/bithum.csv"

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        # 코인 정보
        self.bithum_market = header_to_json(f"{BITHUM_API_URL}/ticker/ALL_KRW")
        # 코인 현재가 
        self.bithum_present_price = header_to_json(f"{BITHUM_API_URL}/ticker/{self.name}_KRW")

    def market_list(self) -> List[str]:
        a = [
            CoinSymbol(coin_symbol=coin).coin_symbol 
            for coin in self.bithum_market["data"]
        ]
        del a[-1]
        return a

    def market_keyvalue(self) -> List[Dict[str, Any]]:
        return csv_read_json(self.data)


class KorbitAPI(ApiBasicArchitecture):
    data: str = f"{PRESENT_DIR}/data/korbit.csv"

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        # 코인 정보 
        self.korbit_market = header_to_json(f"{KOBIT_API_URL}/ticker/detailed/all")
        # 코인 현재가 
        self.korbit_present_price = header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair={self.name.lower()}_krw")

    def market_list(self) -> List[str]:
        return [
            CoinSymbol(coin_symbol=coin.split("_")[0].upper()).coin_symbol 
            for coin in self.korbit_market
        ]

    def market_keyvalue(self) -> List[Dict[str, Any]]:
        return csv_read_json(self.data)


class TotalCoinMarketlistConcatnate(UpbitAPI, BithumAPI, KorbitAPI):
    def __init__(self) -> None:
        super().__init__()

    