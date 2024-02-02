from pydantic import BaseModel

"""
<<<<<< Market Coin Listing DataFormatting >>>>>>
"""

# coin classification data formatting

class MarketDepend(BaseModel):
    upbit: bool
    bithum: bool
    korbit: bool
    coinone: bool


class CoinSymbol(BaseModel):
    coin_symbol: str


class DataFormat(CoinSymbol):
    market_depend: MarketDepend


def coin_classification(
    up: list[str], 
    bit: list[str], 
    kor: list[str], 
    one: list[str], 
    target: str
) -> list[dict[str, str]]:
    market_depend = MarketDepend(
        upbit=(target in up),
        bithum=(target in bit),
        korbit=(target in kor),
        coinone=(target in one)
    )
    return [DataFormat(coin_symbol=target, market_depend=market_depend).model_dump()]