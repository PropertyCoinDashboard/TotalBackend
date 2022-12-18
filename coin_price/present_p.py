import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time
import json
from kafka import KafkaProducer

from api_injection.coin_apis import (
    BithumAPIBitcoin, UpbitAPIBitcoin)
from api_injection.schema import coin_present_schema, concatnate_dictionary


COIN_PRECENT_PRICE = "coin_price"
start_time = time.time()


# 현재가 객체 생성 
upbit = UpbitAPIBitcoin()
bit = BithumAPIBitcoin()

# 로그 생성
present_upbit: dict[str, int] = coin_present_schema(upbit[0], upbit[0]["market"], "opening_price", "trade_price", "high_price", "low_price",
                                    "prev_closing_price", "acc_trade_volume_24h", "acc_trade_price_24h", "timestamp")

present_bithum: dict[str, int] = coin_present_schema(bit["data"], bit.__namesplit__(5), "opening_price", "closing_price", "max_price", "min_price",
                                    "prev_closing_price", "units_traded_24H", "acc_trade_value_24H", "date")


# 스키마 생성
schema = concatnate_dictionary(upbit=present_upbit, bithum=present_bithum)


# print -> log 로 바꿀꺼임 일단 임시로
print(f"end -> {time.time()-start_time}")    

