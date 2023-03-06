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

from .backend_pre.api_injection.coin_apis import * 

bitcoin = CoinMarketBitCoinPresentPrice
ethereum = CoinMarketEthereumPresentPrice
upbit = UpbitAPI
bithum = BithumAPI
korbit = KorbitAPI
