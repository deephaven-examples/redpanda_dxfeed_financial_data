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

types = ['Candle']


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

def clean_candle(input):
    data = {
        "Symbol": input[0],
        "EventFlags": input[1],
        "Index": input[2],
        "Time": input[3],
        "Sequence": input[4],
        "Count": input[5],
        "Open": input[6],
        "High": input[7],
        "Low": input[8],
        "Close": input[9],
        "Volume": input[10],
        "VWap": input[11],
        "BidVolume": input[12],
        "AskVolume": input[13],
        "OpenInterest": input[14],
        "ImpVolatility": input[15]
    }
    producer.produce(topic='Candle', key=None, value=json.dumps(data))
    producer.flush()


while True:
    for obj in my_subscriptions:
        data = obj.handler.get_dataframe().to_json(orient ='values')
        json_dictionary = json.loads(data)
        for key in json_dictionary:
            if(obj.topic_name == 'Candle'):
                formatted = clean_candle(key)
