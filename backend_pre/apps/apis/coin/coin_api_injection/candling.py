import datetime
import time
import requests
import pandas as pd
from typing import *
import plotly.graph_objects as go
from .api_util import header_to_json, making_time
from .api_util import UPBIT_API_URL, BITHUM_API_URL


class ApiBasicArchitecture:
    def __init__(self,
                 name: Optional[str] = None,
                 date: Optional[datetime.datetime] = None,
                 count:  Optional[int] = None) -> None:
        self.name: Optional[str] = name
        self.date: Optional[str] = date
        self.count: Optional[int] = count

    def __namesplit__(self) -> str:
        return self.name.upper()


class BithumCandlingAPI(ApiBasicArchitecture):
    """
    :param minit
        - 차트 간격, 기본값 : 24h {1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h 사용 가능}
    """

    # 시간별 통합으로 되어 있음
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

    def __init__(self, name: Optional[str] = None,
                 date: Optional[datetime.datetime] = None,
                 count: Optional[int] = None) -> None:
        super().__init__(name, date, count)
        self.name_candle_count = f"market=KRW-{self.name}&count={self.count}"
        self.name_candle_count_date = f"market=KRW-{self.name}&to={self.date}&count={self.count}"

    def upbit_candle_price(self, mint: int) -> List:
        return header_to_json(
            f"{UPBIT_API_URL}/candles/minutes/{mint}?{self.name_candle_count}"
        )

    # 상위 200개
    def upbit_candle_day_price(self) -> List:
        return header_to_json(f"{UPBIT_API_URL}/candles/days?{self.name_candle_count}")

    # 날짜 커스텀
    def upbit_candle_day_custom_price(self) -> List:
        return header_to_json(
            f"{UPBIT_API_URL}/candles/days?{self.name_candle_count_date}"
        )


def api_injectional(api: Any, inject_parmeter: Any) -> pd.DataFrame:
    # API 호출
    api_init = api

    api_init = pd.DataFrame(
        inject_parmeter,
        columns=["timestamp", "opening_price", "trade_price",
                 "high_price", "low_price", "candle_acc_trade_volume"]
    )

    api_init["timestamp"] = api_init["timestamp"].apply(
        lambda x: time.strftime(r"%Y-%m-%d %H:%M", time.localtime(x / 1000))
    )

    api_init["opening_price"] = api_init["opening_price"].apply(
        lambda x: float(x))
    api_init["trade_price"] = api_init["trade_price"].apply(lambda x: float(x))
    api_init["high_price"] = api_init["high_price"].apply(lambda x: float(x))
    api_init["low_price"] = api_init["low_price"].apply(lambda x: float(x))

    return api_init


# 결과 출력하기
def upbit_trade_all_list(time_data: List[datetime.datetime]) -> List[pd.DataFrame]:
    timer: List[datetime.datetime] = time_data
    result_upbit_data = []

    for dt in timer:
        try:
            a = dt.strftime("%Y-%m-%d %H:%M:%S")

            upbit_init = UpBitCandlingAPI(
                name="BTC", count=200, date=a
            ).upbit_candle_day_custom_price()

            # API 호출
            maket_init = api_injectional(upbit_init, upbit_init)

            if maket_init.empty:
                continue
            result_upbit_data.append([maket_init])
        except requests.exceptions.JSONDecodeError:
            continue

    return result_upbit_data


# 데이터 병합
def upbit_trade_data_concat(data: List) -> pd.DataFrame:
    result_upbit_data_concat = pd.concat(
        [df for [df] in data], ignore_index=True)
    return result_upbit_data_concat


bithum_init = BithumCandlingAPI(name="BTC").bithum_candle_price(mint="24h")
bithum_init = api_injectional(bithum_init, bithum_init.get("data"))
upbit_init = upbit_trade_all_list(time_data=making_time())
upbit_init = upbit_trade_data_concat(upbit_init)


# bithum_init.to_csv("test.csv", index_label=False, index=False)
# upbit_init.to_csv("upbit_test.csv", index=False, index_label=False)

# fig = go.Figure(layout=go.Layout(title=go.layout.Title(text="Bitcoin -- BTC")))
# fig.add_trace(
#     go.Scatter(
#         x=bithum_init["timestamp"],
#         y=bithum_init["opening_price"],
#         name="bithum",
#         mode="lines",
#     )
# )
# fig.add_trace(
#     go.Scatter(
#         x=upbit_init["timestamp"],
#         y=upbit_init["opening_price"],
#         name="upbit",
#         mode="lines",
#     )
# )
# fig.show()
