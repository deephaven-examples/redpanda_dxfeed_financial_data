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

types = ['Summary']


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

def clean_summary(input):
    data = {
        "Symbol": input[0],
        "DayId": input[1],
        "DayOpenPrice": input[2],
        "DayHighPrice": input[3],
        "DayLowPrice": input[4],
        "DayClosePrice": input[5],
        "PrevDayId": input[6],
        "PrevDayClosePrice": input[7],
        "PrevDayVolume": input[8],
        "OpenInterest": input[9],
        "RawFlags": input[10],
        "ExchangeCode": input[11],
        "DayClosePriceType": input[12],
        "PrevDayClosePriceType": input[13],
        "Scope": input[14]
    }
    producer.produce(topic='Summary', key=None, value=json.dumps(data))
    producer.flush()

while True:
    for obj in my_subscriptions:
        data = obj.handler.get_dataframe().to_json(orient ='values')
        json_dictionary = json.loads(data)
        for key in json_dictionary:
            if(obj.topic_name == 'Summary'):
                formatted = clean_summary(key)
