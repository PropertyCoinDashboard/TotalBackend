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



from typing import Literal, Tuple, Dict, List, Any
import asyncio, json
from kafka import KafkaProducer
from schema.schema import CoinPresentSchema, concatnate_dictionary
from schema.create_log import log
from backend_pre.api_injection.coin_apis import (
      BithumAPI, UpbitAPI, KorbitAPI, header_to_json
)

logging = log()

# kafka and coin information
COIN_API_INJECTION_SYMBOL: Literal = "http://0.0.0.0:8081/coinprice/api-v1/coin/burket"
BOOTSTRAP_SERVER: List[str] = ["kafka1:19091", "kafka2:29092", "kafka3:39093"]
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER, security_protocol="PLAINTEXT")


async def coin_present_price_schema(name: str, api: Dict, data: Tuple[str]) -> Dict[str, int]:
      present_coin: Dict[str, int] = CoinPresentSchema(
            name=name, api=api, data=data).kwargs
      
      return present_coin


async def present(topic_name: str) -> None:
        while True:
            await asyncio.sleep(1)
            # 현재가 객체 생성 
            coin_name: json = header_to_json(COIN_API_INJECTION_SYMBOL)["results"][0]["coin_symbol"]
            
            upbit = UpbitAPI(name=coin_name)
            bithum = BithumAPI(name=coin_name)
            korbit = KorbitAPI(name=coin_name)
            try:
                present_upbit: Dict[str, int] =  await coin_present_price_schema(
                    name=f"upbit-{upbit.__namesplit__()}", api=upbit[0], 
                    data=("opening_price", "trade_price", "high_price", 
                            "low_price", "prev_closing_price", "acc_trade_volume_24h")
                )

                present_bithum: Dict[str, int] = await coin_present_price_schema(
                    name=f"bithum-{bithum.__namesplit__()}", api=bithum["data"],
                    data=("opening_price", "closing_price", "max_price", 
                            "min_price", "prev_closing_price", "units_traded_24H")
                )

                present_korbit: Dict[str, int] = await coin_present_price_schema(
                    name=f"korbit-{korbit.__namesplit__()}", api=korbit[coin_name],
                    data=("open", "last", "bid", 
                            "ask", "low", "volume")
                )
                
                results: List[Dict[str, int]] = [present_upbit, present_bithum, present_korbit]
                
                # # 스키마 생성
                schema: Dict[str, Any]= concatnate_dictionary(upbit=results[0], bithum=results[1], korbit=results[2])
                json_to_schema: bytes = json.dumps(schema).encode("utf-8")
                logging.info(f"데이터 전송 --> \n{json_to_schema}\n")
                producer.send(topic=topic_name, value=json_to_schema)
                
            except KeyError:
                    logging.error(f"에러가 일어났습니다 --> \n{KeyError}\n")

