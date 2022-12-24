import os
import sys
import time
import json
from typing import Final, List
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


from kafka import KafkaProducer
from kafka_distribute.producer import producer_optional

from backend.api_injection.coin_apis import BithumAPI, UpbitAPI, header_to_json
from schema.schema import CoinPresentSchema, concatnate_dictionary


COIN_PRECENT_PRICE: Final[str] = "coin_price"
COIN_API_INJECTION_SYMBOL: Final[str] = "http://0.0.0.0:8081/coinprice/api-v1/coin/burket"
bootstrap_server: List[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=bootstrap_server, security_protocol="PLAINTEXT")


def upbit_schema(upbit: UpbitAPI) -> dict:
      present_upbit: dict[str, int] = CoinPresentSchema(name=upbit[0]["market"], 
                                                        api=upbit[0],
                                                        args=("opening_price", "trade_price", "high_price", "low_price",
                                                            "prev_closing_price", "acc_trade_volume_24h", "acc_trade_price_24h")
                                                      ).kwargs
      return present_upbit
      
      
def bithum_schema(bithum: BithumAPI) -> dict:
      present_bithum: dict[str, int] = CoinPresentSchema(name=bithum.__namesplit__(5), 
                                                      api=bithum["data"], 
                                                      args=("opening_price", "closing_price", "max_price", "min_price",
                                                            "prev_closing_price", "units_traded_24H", "acc_trade_value_24H")
                                                      ).kwargs
      return present_bithum
      
      
while True:
      time.sleep(1)

      coin_name = header_to_json(COIN_API_INJECTION_SYMBOL)[0]["coin_symbol"]

      # 현재가 객체 생성 (나중에 매개변수 받아올것)
      upbit = UpbitAPI(name=coin_name)
      bit = BithumAPI(name=coin_name)

      try:
            present_upbit = upbit_schema(upbit=upbit)
            present_bithum = bithum_schema(bithum=bit)
            # # 스키마 생성
            schema = concatnate_dictionary(upbit=present_upbit, bithum=present_bithum)
            print(schema)
            producer_optional(producer=producer, data=schema, topic=COIN_PRECENT_PRICE)
      except KeyError:
            pass

      

