# 비트코인 현재 시세가 
def bitcoin_present_schema(name: str, api: dict, *args) -> dict:
        data: dict = {
                "name"                 : name,         # 이름
                "opening_price"        : api[args[0]], # 시가
                "closing_price"        : api[args[1]], # 종가
                "max_price"            : api[args[2]], # 저가 
                "min_price"            : api[args[3]], # 고가 
                "timestamp"            : api[args[4]], # 시간
        }
        
        return data


# 코인 현재 시세가 
def coin_present_schema(api: dict, name:str, *args) -> dict:
        data: dict = {
                "market"               : name,                # 이름
                "opening_price"        : api[args[0]],        # 시가
                "closing_price"        : api[args[1]],        # 종가
                "max_price"            : api[args[2]],        # 저가 
                "min_price"            : api[args[3]],        # 고가 
                "prev_closing_price"   : api[args[4]],        # 전일 종가 
                "acc_trade_volume_24h" : api[args[5]],        # 24시간 거래량 
                "acc_trade_price_24h"  : api[args[6]],        # 24시간 거래대금
                "timestamp"            : api[args[7]]         # 시간
        }
    
        return data


def concatnate_dictionary(**kwargs) -> dict: 
        return kwargs