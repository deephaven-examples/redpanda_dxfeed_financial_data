from deephaven import agg as agg

agg_list = [
    agg.min_(["Ask_Min=AskPrice"]),\
    agg.avg(["AskSize_Avg=AskSize"]),\
    agg.max_(["Bid_Max=BidPrice"]), \
    agg.avg(["BidSize_Avg=BidSize"])
]


aggs = quotes.agg_by(agg_list,\
    ["Symbol", "BidExchangeCode", "BidTime", "AskTime"])

related_quotes = trades.aj(quotes, ["Symbol, Timestamp = BidTime"], ["BidTime, BidPrice, BidSize"])
