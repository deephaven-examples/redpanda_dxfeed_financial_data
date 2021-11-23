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

types = ['Profile']


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


def clean_profile(input):
    data = {
        "Symbol": input[0],
        "Beta": input[1],
        "EPS": input[2],
        "DivFreq": input[3],
        "ExdDivAmount": input[4],
        "ExdDivDate": input[5],
        "52HighPrice": input[6],
        "52LowPrice": input[7],
        "Shares": input[8],
        "FreeFloat": input[9],
        "HighLimitPrice": input[10],
        "LowLimitPrice": input[11],
        "HaltStartTime": input[12],
        "HaltEndTime": input[13],
        "Description": input[14],
        "RawFlags": input[15],
        "StatusReason": input[16],
        "TradingStatus": input[17],
        "ShortSaleRestriction": input[18]
    }
    producer.produce(topic='Profile', key=None, value=json.dumps(data))
    producer.flush()

while True:
    for obj in my_subscriptions:
        data = obj.handler.get_dataframe().to_json(orient ='values')
        json_dictionary = json.loads(data)
        for key in json_dictionary:
            if(obj.topic_name == 'Profile'):
                formatted = clean_profile(key)
