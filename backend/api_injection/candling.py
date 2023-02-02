from typing import Any, Optional
from coin_apis import (
    UPBIT_API_URL, BITHUM_API_URL,
    header_to_json, ApiBasicArchitecture
)
import pandas as pd 


class UpBitCandlingAPI(ApiBasicArchitecture):
    """
    :param time 
        minutes, days, weeks, year
        - 분, 일, 주, 년 
    :param minit
        - 시간 단위
    :param count 
        - 얼마나 가져올것인지 
    """
    def __init__(self, name: Optional[str] = None, count: Optional[int] = None) -> None:
        super().__init__(name)
        self.name_candle_count = f'market=KRW-{self.name}&count={count}'
        
    def upbit_candle_price(self, mint: int, count: int) -> list[dict[Any]]:
        return header_to_json(f"{UPBIT_API_URL}/candles/minetes/{mint}?{self.name_candle_count}")

    def upbit_candle_day_price(self) -> list[dict[Any]]:
        return header_to_json(f"{UPBIT_API_URL}/candles/days?{self.name_candle_count}")
    
    def upbit_candle_week_price(self) -> list[dict[Any]]:
        pass
    
    def upbit_candle_year_price(self) -> list[dict[Any]]:
        pass

class BithumCandlingAPI(ApiBasicArchitecture):
    """
    :param minit
        - 차트 간격, 기본값 : 24h {1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h 사용 가능}
    """
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)
    
    # 시간별 통합으로 되어 있음
    def bithum_candle_price(self, mint: str) -> list[dict[Any]]:
        return header_to_json(f"{BITHUM_API_URL}/candlestick/{self.name}_KRW/{mint}")



import time
# c = UpBitCandlingAPI(name="BTC", count=200).upbit_candle_price(mint=5)
# c = pd.DataFrame(c)
# c["timestamp"] = c["timestamp"].apply(lambda x: time.strftime(r'%Y-%m-%d %H:%M', time.localtime(x/1000)))
# a = c.drop(["market", "candle_date_time_utc","candle_date_time_kst","candle_acc_trade_price", "unit"], axis=1)
# data = a[["timestamp", "opening_price", "trade_price", "high_price", "low_price", "candle_acc_trade_volume"]]


# a = BithumCandlingAPI(name="BTC").bithum_candle_price(mint="5m")
# b = pd.DataFrame(a.get("data"), columns=["timestamp", "opening_price", "trade_price", "high_price", "low_price", "candle_acc_trade_volume"])
# b["timestamp"] = b["timestamp"].apply(lambda x: time.strftime(r'%Y-%m-%d %H:%M', time.localtime(x/1000)))
# b["opening_price"] = b["opening_price"].apply(lambda x: float(x))
# b["trade_price"] = b["trade_price"].apply(lambda x: float(x))
# b["high_price"] = b["high_price"].apply(lambda x: float(x))
# b["low_price"] = b["low_price"].apply(lambda x: float(x))


test = UpBitCandlingAPI(name="BTC", count=200).upbit_candle_day_price()
test = pd.DataFrame(test)
test["timestamp"] = test["timestamp"].apply(lambda x: time.strftime(r'%Y-%m-%d %H:%M', time.localtime(x/1000)))
test["candle_acc_trade_price"] = test["candle_acc_trade_price"].apply(lambda x: x/1000000)
print(test)


# import plotly.graph_objects as go
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=b["timestamp"], y=b["opening_price"], mode="lines"))
# fig.add_trace(go.Scatter(x=data["timestamp"], y=data["opening_price"], mode="lines"))
# fig.show()
