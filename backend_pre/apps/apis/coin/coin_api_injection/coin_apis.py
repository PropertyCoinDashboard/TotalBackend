from collections import Counter
from typing import (
    Any, 
    Dict, 
    List, 
    Tuple, 
    Optional, 
    Generator
)

from .api_util import (
    UPBIT_API_URL,
    BITHUM_API_URL,
    KOBIT_API_URL,
    PRESENT_DIR,
)

from .api_util import (
    CoinSymbol,
    CoinKoreaNameSymbol,
    coin_classification,
    header_to_json,
    csv_read_json,
    asdict,
)


class UpbitAPI:
    """
    업비트 API
    """
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name
        self.upbit_market = header_to_json(f"{UPBIT_API_URL}/market/all?isDetails=true")
        self.upbit_coin_present_price = header_to_json(f"{UPBIT_API_URL}/ticker?markets=KRW-{self.name}")

    def market_list(self) -> List[str]:
        return [
            CoinSymbol(coin_symbol=coin["market"].split("-")[1]).coin_symbol
            for coin in self.upbit_market
            if coin["market"].startswith("KRW-")
        ]

    def market_keyvalue(self) -> List[Dict[str, str]]:
        return [
            asdict(
                CoinKoreaNameSymbol(
                    coin_symbol=cv["market"].split("-")[1],
                    korean_name=cv["korean_name"]
                )
            )
            for cv in self.upbit_market
            if cv["market"].startswith("KRW-")
        ]

    def __getitem__(self, index: int) -> Dict:
        return self.upbit_coin_present_price[index]


class BithumAPI:
    """
    빗썸 API
    """
    data: str = f"{PRESENT_DIR}/data/bithum.csv"

    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name
        self.bithum_market = header_to_json(f"{BITHUM_API_URL}/ticker/ALL_KRW")
        self.bithum_present_price = header_to_json(f"{BITHUM_API_URL}/ticker/{self.name}_KRW")

    def market_list(self) -> List[str]:
        return [
            CoinSymbol(coin_symbol=coin).coin_symbol
            for coin in self.bithum_market["data"]
        ][:-1]

    def market_keyvalue(self) -> List[Dict[str, str]]:
        return csv_read_json(self.data)

    def __getitem__(self, index: str) -> Any:
        return self.bithum_present_price[index]


class KorbitAPI:
    """
    코빗 API
    """
    data: str = f"{PRESENT_DIR}/data/korbit.csv"

    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name
        self.korbit_market = header_to_json(f"{KOBIT_API_URL}/ticker/detailed/all")
        if name != None:
            self.korbit_present_price = header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair={self.name.lower()}_krw")

    def market_list(self) -> List[str]:
        return [
            CoinSymbol(coin_symbol=coin.split("_")[0].upper()).coin_symbol
            for coin in self.korbit_market
        ]

    def market_keyvalue(self) -> List[Dict[str, str]]:
        return csv_read_json(self.data)

    def __getitem__(self, index: str) -> Any:
        return header_to_json(f"{KOBIT_API_URL}/ticker/detailed?currency_pair={index.lower()}_krw")


class TotalCoinMarketlistConcatnate:
    def __init__(self) -> None:
        self.upbit_list: List[str] = UpbitAPI().market_list()
        self.bithum_list: List[str] = BithumAPI().market_list()
        self.korbit_list: List[str] = KorbitAPI().market_list()
        
        self.upbit_dict: List[Dict[str, str]] = UpbitAPI().market_keyvalue()
        self.bithum_dict: List[Dict[str, str]] = BithumAPI().market_keyvalue()
        self.korbit_dict: List[Dict[str, str]] = KorbitAPI().market_keyvalue()

    def duplicate_coinsymbol_extract(self) -> List[str]:
        """3개 거래소 동시 상장 심볼 통합 

        Returns:
            List[str]: ["BTC", "ETH" ....]
        """
        concat: List[str] = self.upbit_list + self.bithum_list + self.korbit_list
        duplicate_data: List[Tuple[str, int]] = Counter(concat).most_common()
        result_data: List[str] = [index for index, value in duplicate_data if value == 3]
        
        return result_data

    def duplicate_coinsymbol_name_extract(self) -> List[Dict[str, str]]:
        """거래소 키 밸류 중복 제거 

        Returns:
            List[Dict[str, str]]: [{"coin_symbol": "BTC", "korean_name": "비트코인"}]
        """
        dict_total: List[Dict[str, str]] = self.upbit_dict + self.bithum_dict + self.korbit_dict

        deduplicated_list = []
        for item in dict_total:
            coin_symbol = item['coin_symbol']
            korean_name = item['korean_name']
            if not any(d['coin_symbol'] == coin_symbol for d in deduplicated_list):
                deduplicated_list.append({'coin_symbol': coin_symbol, 'korean_name': korean_name})

        return deduplicated_list

    def coin_classifire(self) -> List[Dict[str, str]]:
        up = self.upbit_list
        bit = self.bithum_list
        kor = self.korbit_list
        coin_info = self.duplicate_coinsymbol_name_extract()

        coin_info_generator: Generator[List[Dict[str, str]], None, None] = (
            coin_classification(
                up=up,
                bit=bit,
                kor=kor,
                target=name["coin_symbol"],
                korean_name=name["korean_name"],
            )
            for name in coin_info
        )

        result: List[Dict[str, str]] = [data for i in coin_info_generator for data in i]

        return result