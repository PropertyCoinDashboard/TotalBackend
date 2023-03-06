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


from typing import Literal


from kafka import KafkaProducer
from backend_pre.api_injection.coin_apis import CoinMarketBitCoinPresentPrice as cp
from schema.schema import BaiscSchema, concatnate_dictionary
from schema.create_log import log


ETHER_TOPIC_NAME: Literal = "trade_ethereum_total"
BOOTSTRAP_SERVER: list[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER, security_protocol="PLAINTEXT")
