from typing import Any, Optional
from coin_apis import (
    UPBIT_API_URL, BITHUM_API_URL,
    header_to_json, ApiBasicArchitecture
)
import multiprocessing as mp
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
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)
        
    def upbit_candle_price(self, type: str,  mint: int, count: int) -> list[dict[Any]]:
        return header_to_json(f"{UPBIT_API_URL}/candles/{type}/{mint}?market=KRW-{self.name}&count={count}")


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
a = BithumCandlingAPI(name="BTC").bithum_candle_price(mint="1m")
b = pd.DataFrame(a.get("data"), columns=["timestamp", "opening_price", "trade_price", "high_price", "low_price", "candle_acc_trade_volume"])
b["timestamp"] = b["timestamp"].apply(lambda x: time.strftime('%Y-%m-%d %H:%M', time.localtime(x/1000)))
b["opening_price"] = b["opening_price"].apply(lambda x: float(x))
b["trade_price"] = b["trade_price"].apply(lambda x: float(x))
b["high_price"] = b["high_price"].apply(lambda x: float(x))
b["low_price"] = b["low_price"].apply(lambda x: float(x))
print(b)

c = UpBitCandlingAPI("BTC").upbit_candle_price(type="minutes", mint=1, count=200)
c = pd.DataFrame(c)
c["timestamp"] = c["timestamp"].apply(lambda x: time.strftime(r'%Y-%m-%d %H:%M', time.localtime(x/1000)))
a = c.drop(["market", "candle_date_time_utc","candle_date_time_kst","candle_acc_trade_price", "unit"], axis=1)
data = a[["timestamp", "opening_price", "trade_price", "high_price", "low_price", "candle_acc_trade_volume"]]
print(data)