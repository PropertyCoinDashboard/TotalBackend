import sys
from pathlib import Path

# 현재 파일의 경로
file_path = Path(__file__).resolve()

# 상위 경로 backend
parent_path = file_path.parent

# 상위 경로 backed_pre -> sys 경로 추가
grandparent_path = parent_path.parent
sys.path.append(str(parent_path))
sys.path.append(str(grandparent_path))


import json, time
from typing import Literal
from concurrent.futures import ThreadPoolExecutor

from kafka import KafkaProducer
from backend_pre.api_injection.coin_apis import CoinMarketBitCoinPresentPrice as cp

from schema.schema import BaiscSchema, concatnate_dictionary
from schema.create_log import log


BIT_TOPIC_NAME: Literal = "trade_bitcoin_total"
BOOTSTRAP_SERVER: list[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER, security_protocol="PLAINTEXT")


# 비트코인 현재가 객체 생성
logging = log()



# 로그 생성
def bitcoin_present_price(name: str, api: dict, data: tuple) -> dict:
      upbit_btc_present: dict = BaiscSchema(name=name, api=api, data=data).kwargs
      return upbit_btc_present


# # 스키마 생성
def schema_flume() -> None:
    with ThreadPoolExecutor() as executor:
        while True:
            try:
                time.sleep(1)
                present = cp()

                # upbit, bithum, kobit 각각의 가격을 병렬처리로 가져옴
                futures = [
                    executor.submit(bitcoin_present_price, name=f"{ex_name}-BTC", api=api_func, data=data)
                    for ex_name, api_func, data in [
                        ("upbit", present.upbit_bitcoin_present_price, ("opening_price", "trade_price", "high_price", "low_price")),
                        ("bithum", present.bithum_bitcoin_present_price, ("opening_price", "closing_price", "max_price", "min_price")),
                        ("kobit", present.korbit_bitcoin_present_price, ("open", "last", "bid", "ask"))
                    ]
                ]

                # futures를 이용하여 각각의 가격을 딕셔너리로 만들고 병합
                schema = concatnate_dictionary(**{ex_name: future.result() for ex_name, future in zip(("upbit", "bithum", "korbit"), futures)})
                json_to_schema = json.dumps(schema).encode("utf-8")
                logging.info(f"데이터 전송 --> \n{json_to_schema}\n")
                producer.send(topic=BIT_TOPIC_NAME, value=json_to_schema)
            except Exception as e:
                logging.error(f"전송 실패 --> {e}")

                  
                  
schema_flume()