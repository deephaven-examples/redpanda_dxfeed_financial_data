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

types = ['TimeAndSale']


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

def clean_timeAndSale(input):
    data = {
        "Symbol": input[0],
        "EventFlags": input[1],
        "Index": input[2],
        "Time": input[3],
        "ExchangeCode": input[4],
        "Price": input[5],
        "Size": input[6],
        "BidPrice": input[7],
        "AskPrice": input[8],
        "ExchangeSaleConditions": input[9],
        "RawFlags": input[10],
        "Buyer": input[11],
        "Seller": input[12],
        "Side": input[13],
        "Type": input[14],
        "IsValidTick": input[15],
        "IsEthTrade": input[16],
        "TradeThroughExempt": input[17],
        "IsSpreadLeg": input[18],
        "Scope": input[19]
    }
    producer.produce(topic='TimeAndSale', key=None, value=json.dumps(data))
    producer.flush()

while True:
    for obj in my_subscriptions:
        data = obj.handler.get_dataframe().to_json(orient ='values')
        json_dictionary = json.loads(data)
        for key in json_dictionary:
            if(obj.topic_name == 'TimeAndSale'):
                formatted = clean_timeAndSale(key)
