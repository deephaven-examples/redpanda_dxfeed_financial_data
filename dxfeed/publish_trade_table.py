from confluent_kafka import Producer
from datetime import datetime
import dxfeed as dx
import json
import time
import re

# Sleep to ensure server has time to run
time.sleep(3)

producer = Producer({
    'bootstrap.servers': 'redpanda:29092',
})

endpoint = dx.Endpoint('demo.dxfeed.com:7300')


symbols = ['SPY', 'AAPL', 'IBM', 'MSFT', 'DIA', 'XLF', 'GOOG', 'AMZN', 'TSLA', 'SPX', 'HPQ', 'CSCO', 'INTC', 'AXP']

types = ['Trade']


class Subscriptions(object):
    def __init__(self, type):
        self.sub = endpoint.create_subscription(type)
        self.handler = dx.DefaultHandler()
        self.sub.set_event_handler(self.handler)
        self.sub = self.sub.add_symbols(symbols)
        self.handler = self.sub.get_event_handler()
        self.topic_name = type

my_subscriptions = []

for i in range(len(types)):
    my_subscriptions.append(Subscriptions(types[i]))

time.sleep(1)

def clean_trades(input):
    data = {
        "Symbol": input[0],
        "Sequence": input[1],
        "Price": input[2],
        "ExchangeCode": input[3],
        "Size": input[4],
        "Tick": input[5],
        "Change"  : input[6],
        "DayVolume": input[7],
        "DayTurnover": input[8],
        "Direction": input[9],
        "Time": input[10],
        "RawFlags": input[11],
        "IsETH": input[12],
        "Scope": input[13]
            }
    producer.produce(topic='Trade', key=None, value=json.dumps(data))
    producer.flush()

while True:
    for obj in my_subscriptions:
        data = obj.handler.get_dataframe().to_json(orient ='values')
        json_dictionary = json.loads(data)
        for key in json_dictionary:
            if(obj.topic_name == 'Trade'):
                formatted = clean_trades(key)
