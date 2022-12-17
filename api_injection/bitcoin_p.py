import time
import json
from typing import Dict, Any, Final
from kafka import KafkaProducer

from coin_apis import (
    BithumAPIBitcoin, UpbitAPIBitcoin
)


BIT_TOPIC_NAME: Final[str] = "trade_bitcoin_total"

bootstrap_server = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=bootstrap_server, security_protocol="PLAINTEXT")

def concatnate() -> None:
    bit = BithumAPIBitcoin().bithum_bitcoin_present_price()
    upbit = UpbitAPIBitcoin().upbit_bitcoin_present_price()
    
    concat_data_bit: Dict[Any, Any] = {"bitthum": bit,
                                        "upbit": upbit}

    while True:
        producer.send(topic=BIT_TOPIC_NAME, value=json.dumps(concat_data_bit).encode("utf-8"))
        producer.flush()
        print(concat_data_bit)
        time.sleep(1)
