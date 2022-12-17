from coin_apis import (
    BithumAPIBitcoin, UpbitAPIBitcoin
)
from fastavro import writer, reader, parse_schema

up = UpbitAPIBitcoin().upbit_present_price()
bit = BithumAPIBitcoin().bithum_present_price()

"""
    schema = {
        'doc': 'A weather reading.',
        'name': 'Weather',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'station', 'type': 'string'},
            {'name': 'time', 'type': 'long'},
            {'name': 'temp', 'type': 'int'},
        ],
    }
    
    records = [
    {u'station': u'011990-99999', u'temp': 0, u'time': 1433269388},
    {u'station': u'011990-99999', u'temp': 22, u'time': 1433270389},
    {u'station': u'011990-99999', u'temp': -11, u'time': 1433273379},
    {u'station': u'012650-99999', u'temp': 111, u'time': 1433275478},
]
"""



