from dataclasses import dataclass
from typing import Any, Dict, Mapping, Tuple

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
class NecessarySchema:
    name: str
    api: Mapping[Any, Any]
    args: Tuple

    def __post_init__(self) -> None:
        self.kwargs = {
            "name": self.name,
            "timestamp": get_utc_time(),
        }


@dataclass
class BasicSchema(NecessarySchema):
    def __post_init__(self) -> None:
        super().__post_init__()

        self.kwargs.update({
            "data": {
                "opening_price": float(self.api[self.args[0]]),
                "closing_price": float(self.api[self.args[1]]),
                "max_price": float(self.api[self.args[2]]),
                "min_price": float(self.api[self.args[3]]),
            }
        })


@dataclass
class CoinPresentSchema(BasicSchema):
    def __post_init__(self) -> None:
        super().__post_init__()

        self.kwargs["data"].update({
            "prev_closing_price": float(self.api[self.args[4]]),
            "acc_trade_volume_24h": float(self.api[self.args[5]]),
        })
