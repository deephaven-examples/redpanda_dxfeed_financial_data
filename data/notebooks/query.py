from deephaven import ComboAggregateFactory as caf

aggs = quotes.by(caf.AggCombo(caf.AggMin("Ask_Min=AskPrice"),caf.AggAvg("AskSize_Avg=AskSize"), caf.AggMax("Bid_Max=BidPrice"), caf.AggAvg("BidSize_Avg=BidSize")), "Symbol", "BidExchangeCode", "BidTime", "AskTime")

relatedQuotes = trades.aj(quotes, "Symbol, Time = BidTime", "BidTime, BidPrice, BidSize")

from deephaven import Plot

plotOHLC = Plot.ohlcPlot("AXP", candle.where("Symbol=`AXP`"), "Time", "Open", "High", "Low", "Close")\
   .chartTitle("AXP")\
   .show()

vWapPlot = Plot.plot("VWAP",candle.where("Symbol=`AAPL`"),"Time","VWap")\
    .show()

plotSingle = Plot.plot("AAPL", trades.where("Symbol = `AAPL`"), "Time", "Price")\
    .show()

from deephaven.MovingAverages import ByEmaSimple

ema_price_10min = ByEmaSimple('BD_SKIP','BD_SKIP','TIME',10,'MINUTES', type='LEVEL')
ema_price_60min =  ByEmaSimple('BD_SKIP','BD_SKIP','TIME',60,'MINUTES', type='LEVEL')
ema_price_100ticks = ByEmaSimple('BD_SKIP','BD_SKIP','TICK',10,None, type='LEVEL')

withEmas = trades.update(\
    "EmaMin10 = ema_price_10min.update(Time, Price, Symbol)",\
    "EmaMin60 = ema_price_60min.update(Time, Price, Symbol)",\
    "EmaTick100 = ema_price_100ticks.update(Time, Price, Symbol)")

from deephaven import Plot
trade_plot = Plot.oneClick(trades, "Symbol")
plot_trades = Plot.plot("Symbol", trade_plot, "Timestamp", "Price").show()