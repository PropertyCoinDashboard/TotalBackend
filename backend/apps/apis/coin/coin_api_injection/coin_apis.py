from collections import Counter
from typing import Any, Tuple, Generator

from .api_util import (
    UPBIT_API_URL,
    BITHUM_API_URL,
    KOBIT_API_URL,
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

    def __init__(self, name: None | str = None) -> None:
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

    def __init__(self, name: None | str = None) -> None:
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

    def __getitem__(self, index: str) -> Any:
        return self.bithum_present_price[index]


class KorbitAPI:
    """
    코빗 API
    """

    def __init__(self, name: None | str = None) -> None:
        self.name = name
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

    def __getitem__(self, index: str) -> Any:
        return header_to_json(
            f"{KOBIT_API_URL}/ticker/detailed?currency_pair={index.lower()}_krw"
        )


class TotalCoinMarketlistConcatnate:
    def __init__(self) -> None:
        self.upbit_list: list[str] = UpbitAPI().market_list()
        self.bithum_list: list[str] = BithumAPI().market_list()
        self.korbit_list: list[str] = KorbitAPI().market_list()

    def duplicate_coinsymbol_extract(self) -> list[str]:
        """3개 거래소 동시 상장 심볼 통합

        Returns:
            list[str]: ["BTC", "ETH" ....]
        """
        concat: list[str] = self.upbit_list + self.bithum_list + self.korbit_list
        duplicate_data: list[Tuple[str, int]] = Counter(concat).most_common()
        result_data: list[str] = [
            index for index, value in duplicate_data if value == 3
        ]

        return result_data

    def coin_classifire(self) -> list[dict[str, str]]:
        """
        코인 분류

        Returns:
            list[dict[str, str]]: 
                >>> [{}]
        """
        up = self.upbit_list
        bit = self.bithum_list
        kor = self.korbit_list
        coin_info = self.duplicate_coinsymbol_extract()

        coin_info_generator: Generator[list[dict[str, str]], None, None] = (
            coin_classification(
                up=up,
                bit=bit,
                kor=kor,
                target=name["coin_symbol"]
            )
            for name in coin_info
        )

        result: list[dict[str, str]] = [data for i in coin_info_generator for data in i]

        return result
