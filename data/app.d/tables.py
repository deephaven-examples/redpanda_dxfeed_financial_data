from deephaven import kafka_consumer as ck
from deephaven.stream.kafka.consumer import TableType, KeyValueSpec
from deephaven import dtypes as dht

trades = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'Trade', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol', dht.string),
    ('Sequence',   dht.int64),
    ('Price',  dht.double),
    ('ExchangeCode',   dht.string),
    ('Size', dht.int64),
    ('Tick',   dht.int64),
    ('Change',  dht.double),
    ('DayVolume',    dht.int64),
    ('DayTurnover',  dht.int64),
    ('Direction',    dht.int64),
    ('Timestamp',    dht.Instant),
    ('RawFlags',  dht.int64),
    ('IsETH',    dht.int64),
    ('Scope',    dht.int64)
    ]),table_type = TableType.append()).sort_descending(["KafkaOffset"])

quotes = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'Quote', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol', dht.string),
    ('Sequence',   dht.int64),
    ('Timestamp',  dht.Instant),
    ('BidTime',   dht.Instant),
    ('BidExchangeCode', dht.string),
    ('BidPrice',   dht.double),
    ('BidSize',  dht.int64),
    ('AskTime',    dht.Instant),
    ('AskExchangeCode',  dht.string),
    ('AskPrice',    dht.double),
    ('AskSize',    dht.int64),
    ('Scope',    dht.int64)
    ]),table_type = TableType.append()).sort_descending(["KafkaOffset"])


candle = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'Candle', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol', dht.string),
    ('EventFlags',   dht.int64),
    ('Index',  dht.int64),
    ('Timestamp',   dht.Instant),
    ('Sequence', dht.int64),
    ('Count',   dht.int64),
    ('Open',  dht.double),
    ('High',    dht.double),
    ('Low',  dht.double),
    ('Close',    dht.double),
    ('Volume',    dht.int64),
    ('VWap',    dht.double),
    ('BidVolume',  dht.int64),
    ('AskVolume',    dht.int64),
    ('OpenInterest',    dht.string),
    ('ImpVolatility',    dht.string)
    ]),table_type = TableType.Append).sort_descending(["KafkaOffset"])



profile = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'Profile', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol', dht.string),
    ('Beta',   dht.double),
    ('EPS',  dht.double),
    ('DivFreq',   dht.int64),
    ('ExdDivAmount', dht.double),
    ('ExdDivDate',   dht.int64),
    ('52HighPrice',  dht.double),
    ('52LowPrice',    dht.double),
    ('Shares',  dht.int64),
    ('FreeFloat',    dht.string),
    ('HighLimitPrice',    dht.double),
    ('LowLimitPrice',    dht.double),
    ('HaltStartTime',  dht.Instant),
    ('HaltEndTime',    dht.Instant),
    ('Description',    dht.string),
    ('RawFlags',    dht.int64),
    ('StatusReason',    dht.string),
    ('TradingStatus',    dht.int64),
    ('ShortSaleRestriction',    dht.int64)
    ]),table_type = TableType.append()).sort_descending(["KafkaOffset"])


summary = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'Summary', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol',    dht.string),
    ('DayId',    dht.int64),
    ('DayOpenPrice',    dht.double),
    ('DayHighPrice',    dht.double),
    ('DayLowPrice',    dht.double),
    ('DayClosePrice',    dht.double),
    ('PrevDayId',    dht.int64),
    ('PrevDayClosePrice',    dht.double),
    ('PrevDayVolume',    dht.int64),
    ('OpenInterest',    dht.int64),
    ('RawFlags',    dht.int64),
    ('ExchangeCode',    dht.string),
    ('DayClosePriceType',    dht.int64),
    ('PrevDayClosePriceType',    dht.int64),
    ('Scope',    dht.int64)
    ]),table_type = TableType.append()).sort_descending(["KafkaOffset"])

order = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'Order', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol',    dht.string),
    ('EventFlags',    dht.int64),
    ('Index',    dht.int64),
    ('Timestamp',    dht.Instant),
    ('Sequence',    dht.int64),
    ('Price',    dht.double),
    ('Size',    dht.int64),
    ('Count',    dht.int64),
    ('Scope',    dht.string),
    ('Side',    dht.string),
    ('ExchangeCode',    dht.string),
    ('Source',    dht.string),
    ('MarketMaker',    dht.string),
    ('SpreadSymbol',    dht.string)
    ]),table_type = TableType.append()).sort_descending(["KafkaOffset"])

underlying = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'Underlying', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol',    dht.string),
    ('Volatility',    dht.double),
    ('FrontVolatility',    dht.double),
    ('BackVolatility',    dht.double),
    ('PutCallRatio',    dht.double)
    ]),table_type = TableType.append()).sort_descending(["KafkaOffset"])

timeAndSale = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'TimeAndSale', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol',    dht.string),
    ('EventFlags',    dht.int64),
    ('Index',    dht.int64),
    ('Timestamp',    dht.Instant),
    ('ExchangeCode',    dht.string),
    ('Price',    dht.double),
    ('Size',    dht.double),
    ('BidPrice',    dht.double),
    ('AskPrice',    dht.double),
    ('ExchangeSaleConditions',    dht.string),
    ('RawFlags',    dht.int64),
    ('Buyer',    dht.string),
    ('Seller',    dht.string),
    ('Side',    dht.int64),
    ('Type',    dht.int64),
    ('IsValidTick',    dht.int64),
    ('IsEthTrade',    dht.int64),
    ('TradeThroughExempt',    dht.int64),
    ('IsSpreadLeg',    dht.int64),
    ('Scope',    dht.int64)
    ]),table_type = TableType.append()).sort_descending(["KafkaOffset"])


series = ck.consume({'bootstrap.servers': 'redpanda:29092'} , 'Series', key_spec=KeyValueSpec.IGNORE, value_spec=ck.json_spec([
    ('Symbol',    dht.string),
    ('EventFlags',    dht.int64),
    ('Index',    dht.int64),
    ('Timestamp',    dht.Instant),
    ('Sequence',    dht.int64),
    ('Expiration',    dht.int64),
    ('Volatility',    dht.double),
    ('PutCallRatio',    dht.double),
    ('ForwardPrice',    dht.double),
    ('Dividend',    dht.double),
    ('Interest',    dht.double)
    ]),table_type = TableType.append()).sort_descending(["KafkaOffset"])

from deephaven import new_table
from deephaven.column import string_col

symbols = new_table([
   string_col("Symbol", ['SPY', 'AAPL', 'IBM', 'MSFT', 'DIA', 'XLF', 'GOOG', 'AMZN', 'TSLA', 'SPX', 'HPQ', 'CSCO', 'INTC', 'AXP'])
   ])
