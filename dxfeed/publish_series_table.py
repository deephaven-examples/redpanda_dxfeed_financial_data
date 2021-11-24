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

types = ['Series']


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

def clean_series(input):
    data = {
        "Symbol": input[0],
        "EventFlags": input[1],
        "Index": input[2],
        "Timestamp": input[3],
        "Sequence": input[4],
        "Expiration": input[5],
        "Volatility": input[6],
        "PutCallRatio": input[7],
        "ForwardPrice": input[8],
        "Dividend": input[9],
        "Interest": input[10]
    }
    producer.produce(topic='Series', key=None, value=json.dumps(data))
    producer.flush()

while True:
    for obj in my_subscriptions:
        data = obj.handler.get_dataframe().to_json(orient ='values')
        json_dictionary = json.loads(data)
        for key in json_dictionary:
            if(obj.topic_name == 'Series'):
                formatted = clean_series(key)
