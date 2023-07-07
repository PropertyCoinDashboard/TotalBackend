from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from collections import Counter

from api_util import (
    UPBIT_API_URL,
    BITHUM_API_URL,
    KOBIT_API_URL,
    PRESENT_DIR,
)
from api_util import (
    CoinSymbol,
    CoinKoreaNameSymbol,
    coin_classification,
    header_to_json,
    csv_read_json,
    asdict,
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
        self.upbit_market = header_to_json(f"{UPBIT_API_URL}/market/all?isDetails=true")
        self.upbit_coin_present_price = header_to_json(f"{UPBIT_API_URL}/ticker?markets=KRW-{self.name}")

    def market_list(self) -> List[str]:
        return [
            CoinSymbol(coin_symbol=coin["market"].split("-")[1]).coin_symbol
            for coin in self.upbit_market
            if coin["market"].startswith("KRW-")
        ]

    def market_keyvalue(self) -> List[Dict[str, Any]]:
        return [
            asdict(
                CoinKoreaNameSymbol(
                    korean_name=cv["market"].split("-")[1],
                    coin_symbol=cv["korean_name"]
                )
            )
            for cv in self.upbit_market
            if cv["market"].startswith("KRW-")
        ]

    def __getitem__(self, index: int) -> Dict:
        return self.upbit_coin_present_price[index]


class BithumAPI(ApiBasicArchitecture):
    data: str = f"{PRESENT_DIR}/data/bithum.csv"

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.bithum_market = header_to_json(f"{BITHUM_API_URL}/ticker/ALL_KRW")
        self.bithum_present_price = header_to_json(f"{BITHUM_API_URL}/ticker/{self.name}_KRW")

    def market_list(self) -> List[str]:
        return [
            CoinSymbol(coin_symbol=coin).coin_symbol
            for coin in self.bithum_market["data"]
        ][:-1]

    def market_keyvalue(self) -> List[Dict[str, Any]]:
        return csv_read_json(self.data)

    def __getitem__(self, index: str) -> Any:
        return self.bithum_present_price[index]


class KorbitAPI(ApiBasicArchitecture):
    data: str = f"{PRESENT_DIR}/data/korbit.csv"

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.korbit_market = header_to_json(f"{KOBIT_API_URL}/ticker/detailed/all")
        self.korbit_present_price = header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair={self.name.lower()}_krw")

    def market_list(self) -> List[str]:
        return [
            CoinSymbol(coin_symbol=coin.split("_")[0].upper()).coin_symbol
            for coin in self.korbit_market
        ]

    def market_keyvalue(self) -> List[Dict[str, Any]]:
        return csv_read_json(self.data)

    def __getitem__(self, index: str) -> Any:
        return header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair={index.lower()}_krw")


class TotalCoinMarketlistConcatnate:
    def __init__(self) -> None:
        self.upbit = UpbitAPI(name="btc")
        self.bithum = BithumAPI(name="btc")
        self.korbit = KorbitAPI(name="btc")
    
    def duplicate_coinsymbol_extract(self) -> List[str]:
        """3개 거래소 동시 상장 심볼 통합 

        Returns:
            List[str]: ["BTC", "ETH" ....]
        """
        u_list = self.upbit.market_list()
        b_list = self.bithum.market_list()
        k_list = self.korbit.market_list()
        
        concat: List[str] = u_list + b_list + k_list
        duplicate_data = Counter(concat).most_common()
        data = [index for index, value in duplicate_data if value == 3]
        return data
 
    def duplicate_coinsymbol_name_extract(self) -> List[Dict[str, str]]:
        """거래소 키 밸류 중복 제거 

        Returns:
            List[Dict[str, str]]: 공사중..
        """
        u_dict = self.upbit.market_keyvalue()
        b_dict = self.bithum.market_keyvalue()
        k_dict = self.korbit.market_keyvalue()
        
        dict_total = u_dict + b_dict + k_dict
        print(dict_total)
        
        
a = TotalCoinMarketlistConcatnate().duplicate_coinsymbol_name_extract()
print(a)