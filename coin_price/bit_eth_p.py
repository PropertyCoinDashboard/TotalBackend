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


import json
import asyncio
from .schema.create_log import log
from .schema.schema import CoinPresentSchema, concatnate_dictionary
from kafka import KafkaProducer
from concurrent.futures import ThreadPoolExecutor
from typing import Literal, Tuple, Dict, List, Any

from backend_pre.apps.apis.coin.coin_api_injection.coin_apis import (
    UpbitAPI, KorbitAPI, BithumAPI
)


BOOTSTRAP_SERVER: List[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER, security_protocol="PLAINTEXT")


# 비트코인 현재가 객체 생성
logging = log()


# 로그 생성
async def present_price_schema(name: str, api: Dict, data: Tuple) -> Dict[str, Any]:
    present: Dict[str, Any] = CoinPresentSchema(name=name, api=api, data=data).kwargs
    return present


# # 스키마 생성
async def schema_flume(coin_name: str, topic_name: Literal) -> None:
    while True:
        await asyncio.sleep(1)
        try:
            with ThreadPoolExecutor() as executor:
                # upbit, bithum, kobit 각각의 가격을 병렬처리로 가져옴
                upbit_api = UpbitAPI(name=coin_name)[0]
                bithum_api = BithumAPI(name=coin_name)["data"]
                korbit_api = KorbitAPI(name=coin_name)[coin_name]
                futures = [
                    asyncio.create_task(present_price_schema(name=f"{ex_name}-{coin_name}", 
                                                             api=api_func, 
                                                             data=data))
                    for ex_name, api_func, data in [
                        ("upbit", upbit_api, ("opening_price", "trade_price", "high_price",
                                              "low_price", "prev_closing_price", "acc_trade_volume_24h")),
                        
                        ("bithum", bithum_api, ("opening_price", "closing_price", "max_price", 
                                                "min_price", "prev_closing_price", "units_traded_24H")),
                        
                        ("korbit", korbit_api, ("open", "last", "bid", 
                                                "ask", "low", "volume"))
                    ]
                ]

                # futures를 이용하여 각각의 가격을 딕셔너리로 만들고 병합
                schema: Dict[str, Any] = concatnate_dictionary(
                    **{ex_name: await future for ex_name, future in zip(("upbit", "bithum", "korbit"), futures)}
                )
                json_to_schema: bytes = json.dumps(schema).encode("utf-8")
                logging.info(f"데이터 전송 --> \n{json_to_schema}\n")
                producer.send(topic=topic_name, value=json_to_schema)
        except Exception as e:
            logging.error(f"전송 실패 --> {e}")
