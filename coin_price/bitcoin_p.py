import os
import sys
from typing import Final, List
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


from kafka import KafkaProducer
from kafka_distribute.producer import producer_optional

from api_injection.coin_apis import CoinMarketBitCoinPresentPrice as cp
from api_injection.schema import BaiscSchema, concatnate_dictionary


BIT_TOPIC_NAME: Final[str] = "trade_bitcoin_total"
bootstrap_server: List[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=bootstrap_server, security_protocol="PLAINTEXT")


# 비트코인 현재가 객체 생성
present = cp()


# 로그 생성
upbit_btc_present: dict = BaiscSchema(
                                    name="upbit-BTC", 
                                    api=present.upbit_bitcoin_present_price, 
                                    args=("timestamp", "opening_price", "trade_price", 
                                          "high_price", "low_price"),
                                    ).kwargs


bithum_btc_present: dict = BaiscSchema(
                                    name="bithum-BTC", 
                                    api=present.bithum_bitcoin_present_price, 
                                    args=("date", "opening_price", "closing_price", 
                                          "max_price", "min_price")
                                    ).kwargs


# # 스키마 생성
schema = concatnate_dictionary(upbit=upbit_btc_present, bithum=bithum_btc_present)
producer_optional(producer=producer, data=schema, topic=BIT_TOPIC_NAME)