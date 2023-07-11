import datetime
import requests
import pandas as pd
from typing import Optional, List, Any
from api_util import header_to_json, making_time
from api_util import UPBIT_API_URL, BITHUM_API_URL


class ApiBasicArchitecture:

    """
    :param minit
        - 차트 간격, 기본값 : 24h {1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h 사용 가능}
    """

    def __init__(
        self,
        name: Optional[str] = None,
        date: Optional[datetime.datetime] = None,
        count: Optional[int] = None,
    ) -> None:
        self.name = name.upper() if name else None
        self.date = date.strftime("%Y-%m-%d %H:%M:%S") if date else None
        self.count = count


class BithumCandlingAPI(ApiBasicArchitecture):
    def bithum_candle_price(self, mint: str) -> List:
        return header_to_json(f"{BITHUM_API_URL}/candlestick/{self.name}_KRW/{mint}")


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
        name: Optional[str] = None,
        date: Optional[datetime.datetime] = None,
        count: Optional[int] = None,
    ) -> None:
        super().__init__(name, date, count)
        self.market_query = f"market=KRW-{self.name}"
        self.count_query = f"count={self.count}"
        self.date_query = f"to={self.date}" if self.date else None

    def upbit_candle_price(self, mint: int) -> List:
        endpoint = f"{UPBIT_API_URL}/candles/minutes/{mint}"
        query = f"{self.market_query}&{self.count_query}"
        return header_to_json(f"{endpoint}?{query}")

    def upbit_candle_day_price(self) -> List:
        endpoint = f"{UPBIT_API_URL}/candles/days"
        query = f"{self.market_query}&{self.count_query}"
        return header_to_json(f"{endpoint}?{query}")

    def upbit_candle_day_custom_price(self) -> List:
        endpoint = f"{UPBIT_API_URL}/candles/days"
        query = f"{self.market_query}&{self.date_query}&{self.count_query}"
        return header_to_json(f"{endpoint}?{query}")


def api_injectional(api: Any, inject_parameter: Any) -> pd.DataFrame:
    api_data = pd.DataFrame(
        inject_parameter,
        columns=[
            "timestamp",
            "opening_price",
            "trade_price",
            "high_price",
            "low_price",
            "candle_acc_trade_volume",
        ],
    )
    api_data["timestamp"] = pd.to_datetime(
        api_data["timestamp"], unit="ms"
    ).dt.strftime("%Y-%m-%d %H:%M")
    api_data["opening_price"] = api_data["opening_price"].astype(float)
    api_data["trade_price"] = api_data["trade_price"].astype(float)
    api_data["high_price"] = api_data["high_price"].astype(float)
    api_data["low_price"] = api_data["low_price"].astype(float)
    return api_data


def upbit_trade_all_list(time_data: List[datetime.datetime]) -> List[pd.DataFrame]:
    result_upbit_data = []

    for dt in time_data:
        try:
            upbit_init = UpBitCandlingAPI(
                name="BTC", count=200, date=dt
            ).upbit_candle_day_custom_price()
            api_data = api_injectional(upbit_init, upbit_init)
            if not api_data.empty:
                result_upbit_data.append(api_data)
        except requests.exceptions.JSONDecodeError:
            continue

    return result_upbit_data


def upbit_trade_data_concat(data: List[pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(data, ignore_index=True)


bithumb_init = BithumCandlingAPI(name="BTC").bithum_candle_price(mint="24h")
bithumb_data = api_injectional(bithumb_init, bithumb_init.get("data"))
upbit_init = upbit_trade_all_list(time_data=making_time())
upbit_data = upbit_trade_data_concat(upbit_init)
