from json import JSONDecodeError
from collections import Counter
from typing import Optional, Tuple, Generator

from .api_util import (
    UPBIT_API_URL,
    BITHUM_API_URL,
    KOBIT_API_URL,
    COINONE_API_URL
)

from .api_util import (
    CoinSymbol,
    coin_classification,
    header_to_json,
)


class UpbitAPI:
    """
    업비트 API
    """

    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name
        self.upbit_market = header_to_json(f"{UPBIT_API_URL}/market/all?isDetails=true")
        self.upbit_coin_present_price = header_to_json(
            f"{UPBIT_API_URL}/ticker?markets=KRW-{self.name}"
        )

    def market_list(self) -> list[str]:
        return [
            CoinSymbol(coin_symbol=coin["market"].split("-")[1]).coin_symbol
            for coin in self.upbit_market
            if coin["market"].startswith("KRW-")
        ]

    def __getitem__(self, index: int) -> dict:
        return self.upbit_coin_present_price[index]


class BithumAPI:
    """
    빗썸 API
    """

    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name
        self.bithum_market = header_to_json(f"{BITHUM_API_URL}/ticker/ALL_KRW")
        self.bithum_present_price = header_to_json(
            f"{BITHUM_API_URL}/ticker/{self.name}_KRW"
        )
    def market_list(self) -> list[str]:
        return [
            CoinSymbol(coin_symbol=coin).coin_symbol
            for coin in self.bithum_market["data"]
        ][:-1]

    def __getitem__(self, index: str) -> dict:
        """
        빗썸 코인 현재가 가지고오기 

        Args:
            index (str): 
                - data -> opening_price 으로 접근
             >>> {'status': '0000', 'data': {'opening_price': '35330000', 'closing_price': '35686000', 'min_price': '35322000', 'max_price': '35760000', 'units_traded': '437.57671276', 'acc_trade_value': '15569572121.8471', 'prev_closing_price': '35330000', 'units_traded_24H': '963.61531872', 'acc_trade_value_24H': '34107287881.5565', 'fluctate_24H': '353000', 'fluctate_rate_24H': '1', 'date': '1695712451453'}}

        Returns:
            Any: 입력한 심볼의 현재가격 
        """
        return self.bithum_present_price[index]


class KorbitAPI:
    """
    코빗 API
    """

    def __init__(self, name: Optional[str] = None) -> None:
        self.name: str = name
        self.korbit_market = header_to_json(f"{KOBIT_API_URL}/ticker/detailed/all")
        if name != None:
            self.korbit_present_price = header_to_json(
                f"{KOBIT_API_URL}/ticker/detailed?currency_pair={self.name.lower()}_krw"
            )

    def market_list(self) -> list[str]:
        return [
            CoinSymbol(coin_symbol=coin.split("_")[0].upper()).coin_symbol
            for coin in self.korbit_market
        ]

    def __getitem__(self, index: str) -> dict:
        """
        코빗 코인 현재가격

        Args:
            index (str): 심볼 입력하면 됨 ex) "etc"

        Returns:
            Any: 입력한 코인읜 현재가격
        """ 
        return header_to_json(
            f"{KOBIT_API_URL}/ticker/detailed?currency_pair={index.lower()}_krw"
        )
    
    
class CoinoneAPI:
    """
    코인원 API
    """
    def __init__(self, name: Optional[str] = None) -> None:
        self.name: str = name
        self.coinone_coin_list = header_to_json(url=f"{COINONE_API_URL}/currencies")
        if name != None:
            self.coinone_present_price = header_to_json(
                f"{COINONE_API_URL}/ticker_new/KRW/{self.name.upper()}?additional_data=false"
            )["tickers"]
    
    def market_list(self) -> list[str]:
        return [
            CoinSymbol(coin_symbol=symbol["symbol"]).coin_symbol
            for symbol in self.coinone_coin_list["currencies"]
        ]
    
    def __getitem__(self, index: int) -> dict:
        return self.coinone_present_price[0]

        


class TotalCoinMarketlistConcatnate:
    def __init__(self) -> None:
        self.upbit_list: list[str] = UpbitAPI().market_list()
        self.bithum_list: list[str] = BithumAPI().market_list()
        self.korbit_list: list[str] = KorbitAPI().market_list()
        self.coinone_list: list[str] = CoinoneAPI().market_list()

    def duplicate_coinsymbol_extract(self) -> list[str]:
        """3개 거래소 동시 상장 심볼 통합

        Returns:
            list[str]: ["BTC", "ETH" ....]
        """
        concat: list[str] = self.upbit_list + self.bithum_list + self.korbit_list + self.coinone_list
        duplicate_data: list[Tuple[str, int]] = Counter(concat).most_common()
        result_data: list[str] = [
            index for index, value in duplicate_data if value == 4
        ]
        return result_data

    def coin_classifire(self) -> list[dict[str, str]]:
        """
        코인 분류

        Returns:
            list[dict[str, str]]: 
                >>> [
                        {
                            "coin_symbol": "BTC",
                            "market_depend": {
                                "upbit": true,
                                "bithum": true,
                                "korbit": true,
                                "coinone": true,
                                }
                        } 
                    ]
        """
        up = self.upbit_list
        bit = self.bithum_list
        kor = self.korbit_list
        one = self.coinone_list
        coin_info = self.duplicate_coinsymbol_extract()

        coin_info_generator: Generator[list[dict[str, str]], None, None] = (
            coin_classification(
                up=up,
                bit=bit,
                kor=kor,
                one=one,
                target=name
            )
            for name in coin_info
        )

        result: list[dict[str, str]] = [data for i in coin_info_generator for data in i]
        return result



def present_price_coin(data: str) -> float:
    """
    해당 코인의 4사 거래소의 평균가를 나타내는 함수 (upbit, bithumb, korbit, coinone)

    Args:
        data (str): 코인 심볼

    Returns:
        float: 평균 가격
    """
    try:
        price = [
            float(UpbitAPI(data)[0]["opening_price"]),
            float(BithumAPI(data)["data"]["opening_price"]),
            float(KorbitAPI(data)[data]["open"]),
            float(CoinoneAPI(data)[0]["first"]),
        ]
        return sum(price) / len(price)
    except (KeyError, JSONDecodeError, AttributeError) as error:
        print("불러오지 못했습니다 에러 --> ", error)


