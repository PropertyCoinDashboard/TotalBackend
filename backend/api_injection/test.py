import candling as cl
import time


time.sleep(1)
u = cl.UpBitCandlingAPI("BTC").upbit_candle_price(type="minutes", mint=1, count=200)

for i in u:
    print(i)
