import time
import datetime
import requests
import pandas as pd
from typing import Any
from api_util import header_to_json, making_time
from api_util import UPBIT_API_URL, BITHUM_API_URL, COINONE_API_URL


class ApiBasicArchitecture:
    """
    기본 클래스
    :param name -> 코인 이름
    :param date -> 날짜
    :param count -> data를 가져올 개수

    __namespace__
        -> coin symbol은 대문자로 취급하기에 소문자가 오더라도 upper로 오류방지
    """

    def __init__(
        self,
        name: None | str = None,
        date: None | datetime.datetime = None,
        count: None | int = None,
    ) -> None:
        self.name: None | str = name
        self.date: None | str = date
        self.count: None | int = count

    def __namesplit__(self) -> str:
        return self.name.upper()


class BithumCandlingAPI(ApiBasicArchitecture):
    """
    :param minit
        - 차트 간격, 기본값 : 24h {1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h 사용 가능}
    """

    # 시간별 통합으로 되어 있음
    def bithum_candle_price(self, mint: str) -> list:
        return header_to_json(
            f"{BITHUM_API_URL}/candlestick/{self.name}_KRW/{mint}"
        )


class CoinoneCandlingAPI(ApiBasicArchitecture):
    """
    :param minit
        - 차트 간격, 기본값 : 24h {1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h 사용 가능}
    """
    
    # 시간별 통합으로 되어 있음
    def coinone_candle_price(self, mint: str) -> list:
        return header_to_json(f"{COINONE_API_URL}/chart/KRW/BTC?interval={mint}")


class UpBitCandlingAPI(ApiBasicArchitecture):
    """
    :param time
        minutes, days, weeks, year
        - 분, 일, 주, 년
    :param minit
        - 시간 단위
    :param count
        - 얼마나 가져올것인지
    :param date
        - 시간 단위
    """

    def __init__(
        self,
        name: None | str = None,
        date: None | datetime.datetime = None,
        count: None | int = None,
    ) -> None:
        super().__init__(name, date, count)
        self.name_candle_count = f"market=KRW-{self.name}&count={self.count}"
        self.name_candle_count_date = (
            f"market=KRW-{self.name}&to={self.date}&count={self.count}"
        )

    def upbit_candle_price(self, mint: int) -> list:
        return header_to_json(
            f"{UPBIT_API_URL}/candles/minutes/{mint}?{self.name_candle_count}"
        )

    # 상위 200개
    def upbit_candle_day_price(self) -> list:
        return header_to_json(
            f"{UPBIT_API_URL}/candles/days?{self.name_candle_count}"
        )

    # 날짜 커스텀
    def upbit_candle_day_custom_price(self) -> list:
        return header_to_json(
            f"{UPBIT_API_URL}/candles/days?{self.name_candle_count_date}"
        )
        

def api_injectional(
    api: Any, 
    inject_parmeter: Any, 
    coin_name: None | str = None
) -> pd.DataFrame:
    # API 호출
    try:
        api_init = api

        api_init = pd.DataFrame(
            inject_parmeter,
            columns=[
                "timestamp",
                "opening_price",
                "trade_price",
                "high_price",
                "low_price",
                "candle_acc_trade_volume",
            ],
        )
        api_init["coin_symbol"] = coin_name
        api_init["timestamp"] = api_init["timestamp"].apply(
            lambda x: time.strftime(r"%Y-%m-%d %H:%M", time.localtime(x / 1000))
        )
        api_init["opening_price"] = api_init["opening_price"].apply(lambda x: float(x))
        api_init["trade_price"] = api_init["trade_price"].apply(lambda x: float(x))
        api_init["high_price"] = api_init["high_price"].apply(lambda x: float(x))
        api_init["low_price"] = api_init["low_price"].apply(lambda x: float(x))
        api_init["candle_acc_trade_volume"] = api_init["candle_acc_trade_volume"].apply(lambda x: float(x))

        time_data = api_init["timestamp"].str.split(" ", expand=True)
        api_init["timestamp"] = time_data[0]

        return pd.DataFrame(api_init)
    except (AttributeError, KeyError):
        print("끝")


# 결과 출력하기
def upbit_trade_all_list(
    time_data: list[datetime.datetime], coin_name: None | str = None
) -> list[pd.DataFrame]:
    timer: list[datetime.datetime] = time_data
    result_upbit_data = []

    for dt in timer:
        try:
            a = dt.strftime("%Y-%m-%d %H:%M:%S")

            upbit_init = UpBitCandlingAPI(
                name=coin_name, count=200, date=a
            ).upbit_candle_day_custom_price()
            # print(coin_name, upbit_init)
            # API 호출
            market_init = api_injectional(upbit_init, upbit_init, coin_name=coin_name)

            if market_init is None:
                continue

            result_upbit_data.append([market_init])
        except requests.exceptions.JSONDecodeError:
            continue

    return result_upbit_data


def transform_coinone_schema(data: pd.DataFrame, coin_name: str) -> pd.DataFrame:
    transformed_data = data.rename(columns={
        "open": "opening_price",
        "high": "high_price",
        "low": "low_price",
        "close": "trade_price",
        "target_volume": "candle_acc_trade_volume"
    })

    transformed_data["coin_symbol"] = coin_name
    transformed_data["opening_price"] = transformed_data["opening_price"].apply(lambda x: float(x))
    transformed_data["trade_price"] = transformed_data["trade_price"].apply(lambda x: float(x))
    transformed_data["high_price"] = transformed_data["high_price"].apply(lambda x: float(x))
    transformed_data["low_price"] = transformed_data["low_price"].apply(lambda x: float(x))
    transformed_data["candle_acc_trade_volume"] = transformed_data["candle_acc_trade_volume"].apply(lambda x: float(x))
    transformed_data["timestamp"] = transformed_data["timestamp"].apply(
        lambda x: time.strftime(r"%Y-%m-%d %H:%M", time.localtime(x / 1000))
    )
    transformed_data: pd.DataFrame = transformed_data.sort_values(by="timestamp", ascending=False).reset_index(drop=True)

    return transformed_data[[
        "timestamp", "opening_price", "trade_price", "high_price", 
        "low_price", "candle_acc_trade_volume", "coin_symbol"
    ]]


def bithum_trade_all_list(coin_name: None | str = None) -> pd.DataFrame:
    bithum_init = BithumCandlingAPI(name=coin_name).bithum_candle_price(mint="24h")
    bithum_init = api_injectional(bithum_init, bithum_init.get("data"), coin_name)
    return bithum_init


def coinone_trade_all_list(coin_name: None | str = None) -> pd.DataFrame:
    coinone_init = CoinoneCandlingAPI(name=coin_name).coinone_candle_price(mint="1d")
    coinone_transformed = transform_coinone_schema(pd.DataFrame(coinone_init["chart"]), coin_name)
    return coinone_transformed


# 데이터 병합
def upbit_trade_data_concat(data: list) -> pd.DataFrame:
    try:
        result_upbit_data_concat = pd.concat([df for [df] in data], ignore_index=True)
        return result_upbit_data_concat
    except ValueError:
        print(f"{data}를 합칠 수 업습니다 비어 있거나 존재하지 않습니다")


def coin_trading_data_concatnate(coin_name: str) -> list[dict]:
    bithum_init = bithum_trade_all_list(coin_name=coin_name)
    upbit_init = upbit_trade_all_list(coin_name=coin_name, time_data=making_time())
    upbit_init = upbit_trade_data_concat(upbit_init)
    coinone_init = coinone_trade_all_list(coin_name=coin_name)

    merge_data: pd.DataFrame = (
        pd.concat([upbit_init, bithum_init, coinone_init], ignore_index=True)
        .groupby(["timestamp", "coin_symbol"])
        .mean()
        .reset_index()
    )
    return merge_data.to_dict(orient="records")
