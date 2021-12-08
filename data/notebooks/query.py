from deephaven import Aggregation as agg, combo_agg

aggs = quotes.aggBy(combo_agg([\
    agg.AggMin("Ask_Min=AskPrice"),\
    agg.AggAvg("AskSize_Avg=AskSize"),\
    agg.AggMax("Bid_Max=BidPrice"), \
    agg.AggAvg("BidSize_Avg=BidSize")]), \
    "Symbol", "BidExchangeCode", "BidTime", "AskTime")

relatedQuotes = trades.aj(quotes, "Symbol, Timestamp = BidTime", "BidTime, BidPrice, BidSize")

from deephaven.MovingAverages import ByEmaSimple

ema_price_10min = ByEmaSimple('BD_SKIP','BD_SKIP','TIME',10,'MINUTES', type='LEVEL')
ema_price_60min =  ByEmaSimple('BD_SKIP','BD_SKIP','TIME',60,'MINUTES', type='LEVEL')
ema_price_100ticks = ByEmaSimple('BD_SKIP','BD_SKIP','TICK',10,None, type='LEVEL')

withEmas = trades.update(\
    "EmaMin10 = ema_price_10min.update(Timestamp, Price, Symbol)",\
    "EmaMin60 = ema_price_60min.update(Timestamp, Price, Symbol)",\
    "EmaTick100 = ema_price_100ticks.update(Timestamp, Price, Symbol)")

from deephaven import Plot

plotOHLC = Plot.ohlcPlot("AXP", candle.where("Symbol=`AXP`"), "Timestamp", "Open", "High", "Low", "Close")\
   .chartTitle("AXP")\
   .show()

vWapPlot = Plot.plot("VWAP",candle.where("Symbol=`AAPL`"),"Timestamp", "VWap")\
    .show()

plotSingle = Plot.plot("AAPL", trades.where("Symbol = `AAPL`"), "Timestamp", "Price")\
    .show()
