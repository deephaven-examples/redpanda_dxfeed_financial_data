from deephaven import ConsumeKafka as ck
from deephaven import Types as dht


trades = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'Trade', key=ck.IGNORE, value=ck.json([
    ('Symbol', dht.string),
    ('Sequence',   dht.int_),
    ('Price',  dht.double),
    ('ExchangeCode',   dht.string),
    ('Size', dht.int_),
    ('Tick',   dht.int_),
    ('Change',  dht.double),
    ('DayVolume',    dht.int_),
    ('DayTurnover',  dht.int_),
    ('Direction',    dht.int_),
    ('Timestamp',    dht.datetime),
    ('RawFlags',  dht.int_),
    ('IsETH',    dht.int_),
    ('Scope',    dht.int_)
    ]),table_type = 'append').sortDescending("KafkaOffset")

quotes = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'Quote', key=ck.IGNORE, value=ck.json([
    ('Symbol', dht.string),
    ('Sequence',   dht.int_),
    ('Timestamp',  dht.datetime),
    ('BidTime',   dht.datetime),
    ('BidExchangeCode', dht.string),
    ('BidPrice',   dht.double),
    ('BidSize',  dht.int_),
    ('AskTime',    dht.datetime),
    ('AskExchangeCode',  dht.string),
    ('AskPrice',    dht.double),
    ('AskSize',    dht.int_),
    ('Scope',    dht.int_)
    ]),table_type = 'append').sortDescending("KafkaOffset")


candle = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'Candle', key=ck.IGNORE, value=ck.json([
    ('Symbol', dht.string),
    ('EventFlags',   dht.int_),
    ('Index',  dht.int64),
    ('Timestamp',   dht.datetime),
    ('Sequence', dht.int_),
    ('Count',   dht.int_),
    ('Open',  dht.double),
    ('High',    dht.double),
    ('Low',  dht.double),
    ('Close',    dht.double),
    ('Volume',    dht.int_),
    ('VWap',    dht.double),
    ('BidVolume',  dht.int_),
    ('AskVolume',    dht.int_),
    ('OpenInterest',    dht.string),
    ('ImpVolatility',    dht.string)
    ]),table_type = 'append').sortDescending("KafkaOffset")



profile = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'Profile', key=ck.IGNORE, value=ck.json([
    ('Symbol', dht.string),
    ('Beta',   dht.double),
    ('EPS',  dht.double),
    ('DivFreq',   dht.int_),
    ('ExdDivAmount', dht.double),
    ('ExdDivDate',   dht.int_),
    ('52HighPrice',  dht.double),
    ('52LowPrice',    dht.double),
    ('Shares',  dht.int_),
    ('FreeFloat',    dht.string),
    ('HighLimitPrice',    dht.double),
    ('LowLimitPrice',    dht.double),
    ('HaltStartTime',  dht.datetime),
    ('HaltEndTime',    dht.datetime),
    ('Description',    dht.string),
    ('RawFlags',    dht.int_),
    ('StatusReason',    dht.string),
    ('TradingStatus',    dht.int_),
    ('ShortSaleRestriction',    dht.int_)
    ]),table_type = 'append').sortDescending("KafkaOffset")


summary = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'Summary', key=ck.IGNORE, value=ck.json([
    ('Symbol',    dht.string),
    ('DayId',    dht.int_),
    ('DayOpenPrice',    dht.double),
    ('DayHighPrice',    dht.double),
    ('DayLowPrice',    dht.double),
    ('DayClosePrice',    dht.double),
    ('PrevDayId',    dht.int_),
    ('PrevDayClosePrice',    dht.double),
    ('PrevDayVolume',    dht.int_),
    ('OpenInterest',    dht.int_),
    ('RawFlags',    dht.int_),
    ('ExchangeCode',    dht.string),
    ('DayClosePriceType',    dht.int_),
    ('PrevDayClosePriceType',    dht.int_),
    ('Scope',    dht.int_)
    ]),table_type = 'append').sortDescending("KafkaOffset")

order = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'Order', key=ck.IGNORE, value=ck.json([
    ('Symbol',    dht.string),
    ('EventFlags',    dht.int_),
    ('Index',    dht.int64),
    ('Timestamp',    dht.datetime),
    ('Sequence',    dht.int_),
    ('Price',    dht.double),
    ('Size',    dht.int_),
    ('Count',    dht.int_),
    ('Scope',    dht.string),
    ('Side',    dht.string),
    ('ExchangeCode',    dht.string),
    ('Source',    dht.string),
    ('MarketMaker',    dht.string),
    ('SpreadSymbol',    dht.string)
    ]),table_type = 'append').sortDescending("KafkaOffset")

underlying = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'Underlying', key=ck.IGNORE, value=ck.json([
    ('Symbol',    dht.string),
    ('Volatility',    dht.double),
    ('FrontVolatility',    dht.double),
    ('BackVolatility',    dht.double),
    ('PutCallRatio',    dht.double)
    ]),table_type = 'append').sortDescending("KafkaOffset")

timeAndSale = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'TimeAndSale', key=ck.IGNORE, value=ck.json([
    ('Symbol',    dht.string),
    ('EventFlags',    dht.int_),
    ('Index',    dht.int64),
    ('Timestamp',    dht.datetime),
    ('ExchangeCode',    dht.string),
    ('Price',    dht.double),
    ('Size',    dht.double),
    ('BidPrice',    dht.double),
    ('AskPrice',    dht.double),
    ('ExchangeSaleConditions',    dht.string),
    ('RawFlags',    dht.int_),
    ('Buyer',    dht.string),
    ('Seller',    dht.string),
    ('Side',    dht.int_),
    ('Type',    dht.int_),
    ('IsValidTick',    dht.int_),
    ('IsEthTrade',    dht.int_),
    ('TradeThroughExempt',    dht.int_),
    ('IsSpreadLeg',    dht.int_),
    ('Scope',    dht.int_)
    ]),table_type = 'append').sortDescending("KafkaOffset")


series = ck.consumeToTable({'bootstrap.servers': 'redpanda:29092'} , 'Series', key=ck.IGNORE, value=ck.json([
    ('Symbol',    dht.string),
    ('EventFlags',    dht.int_),
    ('Index',    dht.int64),
    ('Timestamp',    dht.datetime),
    ('Sequence',    dht.int_),
    ('Expiration',    dht.int_),
    ('Volatility',    dht.double),
    ('PutCallRatio',    dht.double),
    ('ForwardPrice',    dht.double),
    ('Dividend',    dht.double),
    ('Interest',    dht.double)
    ]),table_type = 'append').sortDescending("KafkaOffset")


symbols = None

symbols = trades.selectDistinct("Symbol")

from deephaven import Plot
trade_plot = Plot.oneClick(trades, "Symbol")
