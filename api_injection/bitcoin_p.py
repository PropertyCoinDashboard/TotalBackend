import time
import json
from typing import Final

from kafka import KafkaProducer
from coin_apis import CoinMarketBitCoinPresentPrice as cp
from schema import bitcoin_present_schema, concatnate_dictionary


BIT_TOPIC_NAME: Final[str] = "trade_bitcoin_total"
bootstrap_server = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=bootstrap_server, security_protocol="PLAINTEXT")


# 비트코인 현재가 객체 생성
present = cp()


# 로그 생성
upbit_btc_present = bitcoin_present_schema("upbit-BTC", present.upbit_bitcoin_present_price, 
                           "opening_price", "trade_price", "high_price", "low_price", "timestamp")

bithum_btc_present = bitcoin_present_schema("bithum-BTC", present.bithum_bitcoin_present_price, 
                            "opening_price", "closing_price", "max_price", "min_price", "date")


# 스키마 생성
schma = concatnate_dictionary(upbit=upbit_btc_present, bithum=bithum_btc_present)


while True:
    producer.send(topic=BIT_TOPIC_NAME, value=json.dumps(schma).encode("utf-8"))
    producer.flush()
    print(schma)
    time.sleep(1)



