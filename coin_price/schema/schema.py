from dataclasses import dataclass
from typing import Any, Mapping

from datetime import timezone
import datetime
  

def utc_time() -> int:
        # Getting the current date
        # and time
        dt = datetime.datetime.now(timezone.utc)
        
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        
        return utc_timestamp


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
        
        
class BaiscSchema(NescessarySchema):    
        """
        로그 건들지 말것
        """ 
        def __init__(self, name: str, api: dict, args: tuple) -> None:
                self.kwargs = {
                        "name"                 : name,         # 이름
                        "timestamp"            : utc_time(), # 시간
                        "opening_price"        : api[args[0]], # 시가
                        "closing_price"        : api[args[1]], # 종가
                        "max_price"            : api[args[2]], # 저가 
                        "min_price"            : api[args[3]], # 고가 
                }


class CoinPresentSchema(BaiscSchema): 
        """
        로그 건들지 말것
        """ 
        def __init__(self, name: str, api: dict, args: tuple) -> None:
                super().__init__(name, api, args)
                self.kwargs.update({
                        "prev_closing_price"   : api[args[4]],        # 전일 종가 
                        "acc_trade_volume_24h" : api[args[5]],        # 24시간 거래량 
                        "acc_trade_price_24h"  : api[args[6]],  
                })


def concatnate_dictionary(**kwargs): 
        """
        dictionary 합침
        """
        return kwargs

