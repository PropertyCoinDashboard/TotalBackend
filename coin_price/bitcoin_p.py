import os
import sys
from typing import Final, List
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


from kafka import KafkaProducer
from kafka_distribute.producer import producer_optional

from backend.api_injection.coin_apis import CoinMarketBitCoinPresentPrice as cp
from schema.schema import BaiscSchema, concatnate_dictionary
from schema.create_log import log


BIT_TOPIC_NAME: Final[str] = "trade_bitcoin_total"
bootstrap_server: List[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=bootstrap_server, security_protocol="PLAINTEXT")


# 비트코인 현재가 객체 생성
logging = log()


# 로그 생성
def bitcoin_present_price(name: str, api: dict, data: tuple) -> dict:
      upbit_btc_present: dict = BaiscSchema(name=name, api=api, data=data).kwargs
      return upbit_btc_present


# # 스키마 생성
while True:
      present = cp()
      
      upbit_btc: dict = bitcoin_present_price(name="upbit-BTC", 
                                        api=present.upbit_bitcoin_present_price, 
                                        data=("opening_price", "trade_price", "high_price", "low_price"))
      
      bithum_btc: dict = bitcoin_present_price(name="bithum-BTC", 
                                         api=present.bithum_bitcoin_present_price, 
                                         data=("opening_price", "closing_price", "max_price", "min_price"))
      
      
      schema: dict[dict[str, int, float]] = concatnate_dictionary(upbit=upbit_btc, bithum=bithum_btc)
      logging.info(f"데이터 전송 --> \n{schema}\n")
      producer_optional(producer=producer, data=schema, topic=BIT_TOPIC_NAME)