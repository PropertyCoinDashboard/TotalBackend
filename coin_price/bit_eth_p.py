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

from schema.create_log import log
from schema.schema import CoinPresentSchema
from kafka import KafkaProducer
from concurrent.futures import ThreadPoolExecutor
from typing import Literal, Tuple, Dict, List, Any

from backend_pre.apps.apis.coin.coin_api_injection.coin_apis import (
    UpbitAPI,
    KorbitAPI,
    BithumAPI,
)
from dataclasses import dataclass


BOOTSTRAP_SERVER: List[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER, security_protocol="PLAINTEXT"
)


# 비트코인 현재가 객체 생성
logging = log()


# 로그 생성
async def present_price_schema(name: str, api: Dict, data: Tuple) -> Dict[str, Any]:
    present: Dict[str, Any] = CoinPresentSchema(name=name, api=api, data=data).kwargs
    return present


@dataclass
class PriceSchema:
    upbit: Dict[str, Any]
    bithum: Dict[str, Any]
    korbit: Dict[str, Any]

    @classmethod
    async def get_upbit_data(cls, coin_name: str) -> Dict[str, Any]:
        # upbit 데이터를 얻는 비동기 작업
        upbit_api = UpbitAPI(name=coin_name)[0]
        return await present_price_schema(
            name=f"upbit-{coin_name}",
            api=upbit_api,
            data=(
                "opening_price",
                "trade_price",
                "high_price",
                "low_price",
                "prev_closing_price",
                "acc_trade_volume_24h",
            ),
        )

    @classmethod
    async def get_bithum_data(cls, coin_name: str) -> Dict[str, Any]:
        # bithum 데이터를 얻는 비동기 작업
        bithum_api = BithumAPI(name=coin_name)["data"]
        return await present_price_schema(
            name=f"bithum-{coin_name}",
            api=bithum_api,
            data=(
                "opening_price",
                "closing_price",
                "max_price",
                "min_price",
                "prev_closing_price",
                "units_traded_24H",
            ),
        )

    @classmethod
    async def get_korbit_data(cls, coin_name: str) -> Dict[str, Any]:
        # korbit 데이터를 얻는 비동기 작업
        korbit_api = KorbitAPI(name=coin_name)[coin_name]
        return await present_price_schema(
            name=f"korbit-{coin_name}",
            api=korbit_api,
            data=("open", "last", "bid", "ask", "low", "volume"),
        )

    @classmethod
    async def schema_flume(cls, coin_name: str, topic_name: Literal) -> None:
        while True:
            await asyncio.sleep(1)
            try:
                with ThreadPoolExecutor() as executor:
                    futures = [
                        asyncio.create_task(cls.get_upbit_data(coin_name)),
                        asyncio.create_task(cls.get_bithum_data(coin_name)),
                        asyncio.create_task(cls.get_korbit_data(coin_name)),
                    ]

                    schema = cls(
                        upbit=await futures[0],
                        bithum=await futures[1],
                        korbit=await futures[2],
                    )

                    json_to_schema: bytes = json.dumps(schema.__dict__).encode("utf-8")
                    logging.info(f"데이터 전송 --> \n{json_to_schema}\n")
                    producer.send(topic=topic_name, value=json_to_schema)
            except Exception as e:
                logging.error(f"전송 실패 --> {e}")
