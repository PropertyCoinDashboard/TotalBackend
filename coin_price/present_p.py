import os
import sys
import json, time
from typing import Final, List
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


from kafka import KafkaProducer
from kafka_distribute.producer import producer_optional

from backend.api_injection.coin_apis import (
      BithumAPI, UpbitAPI, KorbitAPI, header_to_json)
from schema.schema import CoinPresentSchema, concatnate_dictionary
from schema.create_log import log
logging = log()


COIN_PRECENT_PRICE: Final[str] = "coin_price"
COIN_API_INJECTION_SYMBOL: Final[str] = "http://0.0.0.0:8081/coinprice/api-v1/coin/burket"

# kafka
# bootstrap_server: List[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
# producer = KafkaProducer(bootstrap_servers=bootstrap_server, security_protocol="PLAINTEXT")


def coin_present_price_schema(name: str, api: dict, data: tuple[str]) -> dict[str, int]:
      present_coin: dict[str, int, float] = CoinPresentSchema(
            name=name, api=api, data=data).kwargs
      
      return present_coin


while True:
      # time.sleep(1)
      # 현재가 객체 생성 
      coin_name: json = header_to_json(COIN_API_INJECTION_SYMBOL)[0]["coin_symbol"]

      upbit = UpbitAPI(name=coin_name)
      bithum = BithumAPI(name=coin_name)
      korbit = KorbitAPI(name=coin_name)
      try:
            present_upbit: dict = coin_present_price_schema(
                  name=upbit.__namesplit__(), api=upbit[0], 
                  data=("opening_price", "trade_price", "high_price", 
                        "low_price", "prev_closing_price", "acc_trade_volume_24h")
            )

            present_bithum: dict = coin_present_price_schema(
                  name=bithum.__namesplit__(), api=bithum["data"],
                  data=("opening_price", "closing_price", "max_price", 
                        "min_price", "prev_closing_price", "units_traded_24H")
            )

            present_korbit: dict = coin_present_price_schema(
                  name=korbit.__namesplit__(), api=korbit[coin_name],
                  data=("open", "last", "bid", 
                        "ask", "low", "volume")
            )
            
            # # 스키마 생성
            schema: dict[str, int]= concatnate_dictionary(upbit=present_upbit, bithum=present_bithum, korbit=present_korbit)
            logging.info(f"데이터 전송 --> \n{json.dumps(schema)}\n")
            # producer_optional(producer=producer, data=schema, topic=COIN_PRECENT_PRICE)
            
      except KeyError:
            logging.error(f"에러가 일어났습니다 --> \n{KeyError}\n")
            pass

      

