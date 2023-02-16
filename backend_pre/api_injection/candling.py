from typing import Any, Optional, List, Tuple
from coin_apis import (
    UPBIT_API_URL, BITHUM_API_URL,
    header_to_json, ApiBasicArchitecture
)
import pandas as pd 
'https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&count=1'
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
        self.count = count
        self.name_candle_count = f'market=KRW-{self.name}&count={self.count}'
        
    def upbit_candle_price(self, mint: int) -> list[dict[Any]]:
        return header_to_json(f"{UPBIT_API_URL}/candles/minutes/{mint}?{self.name_candle_count}")

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
c = UpBitCandlingAPI(name="BTC", count=200).upbit_candle_price(mint=5)
c = pd.DataFrame(c)
c["timestamp"] = c["timestamp"].apply(lambda x: time.strftime(r'%Y-%m-%d %H:%M', time.localtime(x/1000)))
a = c.drop(["market", "candle_date_time_utc","candle_date_time_kst","candle_acc_trade_price", "unit"], axis=1)
data = a[["timestamp", "opening_price", "trade_price", "high_price", "low_price", "candle_acc_trade_volume"]]


a = BithumCandlingAPI(name="BTC").bithum_candle_price(mint="5m")
b = pd.DataFrame(a.get("data"), columns=["timestamp", "opening_price", "trade_price", "high_price", "low_price", "candle_acc_trade_volume"])
b["timestamp"] = b["timestamp"].apply(lambda x: time.strftime(r'%Y-%m-%d %H:%M', time.localtime(x/1000)))
b["opening_price"] = b["opening_price"].apply(lambda x: float(x))
b["trade_price"] = b["trade_price"].apply(lambda x: float(x))
b["high_price"] = b["high_price"].apply(lambda x: float(x))
b["low_price"] = b["low_price"].apply(lambda x: float(x))


# test = UpBitCandlingAPI(name="BTC", count=200).upbit_candle_day_price()
# test = pd.DataFrame(test)
# test["timestamp"] = test["timestamp"].apply(lambda x: time.strftime(r'%Y-%m-%d %H:%M', time.localtime(x/1000)))
# test["candle_acc_trade_price"] = test["candle_acc_trade_price"].apply(lambda x: x/1000000)


# import plotly.graph_objects as go
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=b["timestamp"], y=b["opening_price"], mode="lines"))
# fig.add_trace(go.Scatter(x=data["timestamp"], y=data["opening_price"], mode="lines"))
# fig.show()

def merge_candles(upbit_candles: List[Tuple[float, float, float, float]], 
                  bithumb_candles: List[Tuple[float, float, float, float]]) -> List[Tuple[int, float]]:
    # upbit_candles와 bithumb_candles를 타임스탬프 기준으로 정렬하고, 가격 평균을 구해서 리스트로 반환하는 함수
    # upbit_candles: Upbit에서 가져온 캔들 데이터 리스트
    # bithumb_candles: Bithumb에서 가져온 캔들 데이터 리스트
    
    # 각 캔들 데이터에 타임스탬프를 추가한다
    upbit_candles_with_timestamp = [(candle[0], *candle[1:]) for candle in upbit_candles]
    bithumb_candles_with_timestamp = [(candle[0], *candle[1:]) for candle in bithumb_candles]
    # # 타임스탬프를 기준으로 정렬한다
    # sorted_candles = sorted(upbit_candles_with_timestamp + bithumb_candles_with_timestamp, key=lambda x: x[0])
    
    # result = []
    # cur_timestamp = sorted_candles[0][0]
    # cur_candles = []
    
    # # 캔들 데이터를 하나씩 처리하면서 가격 평균을 계산한다
    # for candle in sorted_candles:
    #     if candle[0] != cur_timestamp:
    #         # 이전 타임스탬프에서 가격 평균을 구해서 result에 추가한다
    #         if cur_candles:
    #             avg_price = sum(price for _, price in cur_candles) / len(cur_candles)
    #             result.append((cur_timestamp, avg_price))
    #         # 새로운 타임스탬프를 처리하기 위해 cur_candles와 cur_timestamp를 초기화한다
    #         cur_timestamp = candle[0]
    #         cur_candles = []
    #     cur_candles.append(candle[1:])
    
    # # 마지막 타임스탬프에서 가격 평균을 구해서 result에 추가한다
    # if cur_candles:
    #     avg_price = sum(price for _, price in cur_candles) / len(cur_candles)
    #     result.append((cur_timestamp, avg_price))
    
    # return result
