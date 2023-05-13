from dataclasses import dataclass
from typing import *

import datetime


def get_utc_time():
    utc_now = datetime.datetime.utcnow()
    return utc_now.timestamp()


def concatnate_dictionary(**kwargs: Dict) -> Dict[str, Dict]:
    """
    dictionary 합침
    """
    return kwargs


@dataclass
class NescessarySchema:
    """
    data type
    로그 데이터 포맷   
    :param = name: str
    :param = api: dict
    :param = args : tuple
    """
    name: str
    api: Mapping[Any, Any]
    args: tuple

    def __init__(self, name: str) -> None:
        self.kwargs = {
            "name": name,              # 이름
            "timestamp": get_utc_time(),        # 시간
        }


class BaiscSchema(NescessarySchema):
    """
    로그 건들지 말것
    """

    def __init__(self, name: str, api: Dict, data: Tuple) -> None:
        super().__init__(name)

        self.kwargs.update({
            "data": {
                "opening_price": float(api[data[0]]),  # 시가
                "closing_price": float(api[data[1]]),  # 종가
                "max_price": float(api[data[2]]),  # 저가
                "min_price": float(api[data[3]]),  # 고가
            }
        })


class CoinPresentSchema(BaiscSchema):
    """
    로그 건들지 말것
    """

    def __init__(self, name: str, api: Dict, data: Tuple) -> None:
        super().__init__(name, api, data)
        self.kwargs["data"].update({
            "prev_closing_price": float(api[data[4]]),        # 전일 종가
            "acc_trade_volume_24h": float(api[data[5]]),      # 24시간 거래량
            # "acc_trade_price_24h"  : float(api[data[6]]),      # 24시간 금액량
        })
