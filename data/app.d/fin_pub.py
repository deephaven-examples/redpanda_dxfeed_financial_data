from confluent_kafka import Producer
from datetime import datetime
import dxfeed as dx
import json
import time
import re

producer = Producer({
    'bootstrap.servers': 'localhost:9092',
})

endpoint = dx.Endpoint('demo.dxfeed.com:7300')


symbols = ['SPY', 'AAPL', 'IBM', 'MSFT', 'DIA', 'XLF', 'GOOG', 'AMZN', 'TSLA', 'SPX', 'HPQ', 'CSCO', 'INTC', 'AXP']

types = ['Trade', 'Quote', 'Candle', 'Profile', 'Summary', 'Order', 'Underlying', 'TimeAndSale', 'Series']


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

time.sleep(3)

def clean_trades(input):
    output = {
    "Symbol": input[0].replace("\"",""),
    "Sequence": input[1],
    "Price": input[2],
    "ExchangeCode": input[3].replace("\"",""),
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
    return output

def clean_quote(input):
    output = {
    "Symbol": input[0].replace("\"",""),
    "Sequence": input[1],
    "Time": input[2],
    "BidTime": input[3],
    "BidExchangeCode": input[4].replace("\"",""),
    "BidPrice": input[5],
    "BidSize": input[6],
    "AskTime": input[7],
    "AskExchangeCode": input[8].replace("\"",""),
    "AskPrice": input[9],
    "AskSize": input[10],
    "Scope": input[11]
    }
    return output

def clean_candle(input):
    output = {
    "Symbol": input[0].replace("\"",""),
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
    return output

def clean_profile(input):
    output = {
    "Symbol": input[0].replace("\"",""),
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
    "Description": input[14].replace("\"",""),
    "RawFlags": input[15],
    "StatusReason": input[16].replace("\"",""),
    "TradingStatus": input[17],
    "ShortSaleRestriction": input[18]
    }
    return output

def clean_summary(input):
    output = {
    "Symbol": input[0].replace("\"",""),
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
    "ExchangeCode": input[11].replace("\"",""),
    "DayClosePriceType": input[12],
    "PrevDayClosePriceType": input[13],
    "Scope": input[14]
    }
    return output

def clean_order(input):
    output = {
    "Symbol": input[0].replace("\"",""),
    "EventFlags": input[1],
    "Index": input[2],
    "Time": input[3],
    "Sequence": input[4],
    "Price": input[5],
    "Size": input[6],
    "Count": input[7],
    "Scope": input[8],
    "Side": input[9],
    "ExchangeCode": input[10].replace("\"",""),
    "Source": input[11].replace("\"",""),
    "MarketMaker": input[12].replace("\"",""),
    "SpreadSymbol": input[13].replace("\"","")
    }
    return output

def clean_underlying(input):
    output = {
    "Symbol": input[0].replace("\"",""),
    "Volatility": input[1],
    "FrontVolatility": input[2],
    "BackVolatility": input[3],
    "PutCallRatio": input[4]
    }
    return output

def clean_timeAndSale(input):
    output = {
    "Symbol": input[0].replace("\"",""),
    "EventFlags": input[1],
    "Index": input[2],
    "Time": input[3],
    "ExchangeCode": input[4].replace("\"",""),
    "Price": input[5],
    "Size": input[6],
    "BidPrice": input[7],
    "AskPrice": input[8],
    "ExchangeSaleConditions": input[9].replace("\"",""),
    "RawFlags": input[10],
    "Buyer": input[11].replace("\"",""),
    "Seller": input[12].replace("\"",""),
    "Side": input[13],
    "Type": input[14],
    "IsValidTick": input[15],
    "IsEthTrade": input[16],
    "TradeThroughExempt": input[17],
    "IsSpreadLeg": input[18],
    "Scope": input[19]
    }
    return output

def clean_series(input):
    output = {
    "Symbol": input[0].replace("\"",""),
    "EventFlags": input[1],
    "Index": input[2],
    "Time": input[3],
    "Sequence": input[4],
    "Expiration": input[5],
    "Volatility": input[6],
    "PutCallRatio": input[7],
    "ForwardPrice": input[8],
    "Dividend": input[9],
    "Interest": input[10]
    }
    return output

while True:
    for obj in my_subscriptions:
        data = obj.handler.get_dataframe().tail(1).to_json(orient ='values')
        if(obj.topic_name == 'Trade'):
            formatted = clean_trades(data.replace("[","").replace("]","").split(","))
        if(obj.topic_name == 'Quote'):
            formatted = clean_quote(data.replace("[","").replace("]","").split(","))
        if(obj.topic_name == 'Candle'):
            formatted = clean_candle(data.replace("[","").replace("]","").split(","))
        if(obj.topic_name == 'Profile'):
            formatted = clean_profile(data.replace("[","").replace("]","").split(","))
        if(obj.topic_name == 'Summary'):
            formatted = clean_summary(data.replace("[","").replace("]","").split(","))
        if(obj.topic_name == 'Order'):
            formatted = clean_order(data.replace("[","").replace("]","").split(","))
        if(obj.topic_name == 'Underlying'):
            formatted = clean_underlying(data.replace("[","").replace("]","").split(","))
        if(obj.topic_name == 'TimeAndSale'):
            formatted = clean_timeAndSale(data.replace("[","").replace("]","").split(","))
        if(obj.topic_name == 'Series'):
            formatted = clean_series(data.replace("[","").replace("]","").split(","))
        producer.produce(topic=obj.topic_name, key=None, value=json.dumps(formatted))
        producer.flush()


#for obj in my_subscriptions:
#    print(obj.sub.close_subscription())

#endpoint.close_connection()
