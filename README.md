# redpanda_dxfeed_financial_data

This repository shows you how to use [Redpanda](https://vectorized.io/) to stream [dxFeed](https://dxfeed.com/) demo data into Deephaven. It uses an example producer, created in the python application fin_pub.py.

## How it works

### Deephaven application mode

This app runs using [Deephaven's application mode](https://deephaven.io/core/docs/how-to-guides/app-mode/).


### Components

* `Dockerfile` - The dockerfile for the application. This extends the default Deephaven image to add dependencies. See our guide, [How to install Python packages](https://deephaven.io/core/docs/how-to-guides/install-python-packages/#add-packages-to-a-custom-docker-image), for more information.
* `docker-compose.yml` - The Docker Compose file for the application. This is mostly the same as the [Deephaven docker-compose file](https://raw.githubusercontent.com/deephaven/deephaven-core/main/containers/python-examples/docker-compose.yml) with modifications to run Redpanda, application mode, and the custom dependencies.
* `RedpandaStart.sh` - A simple helper script to launch the application.
* `app.d/app.app` - The Deephaven application mode app file.
* `app.d/requirements.txt` - Python dependencies for the application.
* `app.d/fin_pub.py` - The Python script that pulls the data from [dxFeed](https://dxfeed.com/) and streams to [Redpanda](https://vectorized.io/).


### High level overview

The demo feed contains a handful of symbols with 15 minute delayed publication during trading hours. In order to provide events during non-trading hours, the demo feed will replay random old events every few seconds.

The Repanda Kafka producer used in this guide creates the following Deephaven tables:

```python
'trade', 'quote', 'candle', 'profile', 'summary', 'order', 'underlying', 'timeAndSale', 'series'
```

With have the symbols:

```python
symbols = ['SPY', 'AAPL', 'IBM', 'MSFT', 'DIA', 'XLF', 'GOOG', 'AMZN', 'TSLA', 'SPX', 'HPQ', 'CSCO', 'INTC', 'AXP']
```

## Dependencies

* The [Deephaven-core dependencies](https://github.com/deephaven/deephaven-core#required-dependencies) are required for this project.

## Launch

To launch the latest release, you can clone the repository via:

```shell
git clone https://github.com/deephaven-examples/redpanda_dxfeed_financial_data.git
cd redpanda_dxfeed_financial_data
```

A start script will install the needed python modules. It will also start the Deephaven IDE, Redpanda images and execute the python application to produce the stream from dxFeed.

To run it, execute:

```shell
./RedpandaStart.sh
```

Go to [http://localhost:10000/ide](http://localhost:10000/ide) to view the tables in the top right **Panels** tab!

### Perform aggregations

We can then write other queries which combine and/or aggregate data from these streams. This query uses an [as-of join](https://deephaven.io/core/docs/reference/table-operations/join/aj/) to correlate trade events with the most recent bid for the same symbol.

```python skip-test
relatedQuotes = trades.aj(quotes, "Sym,Time=BidTime", "BidTime,BidPrice,BidSize,BidExchange")
```

The next query calculates the volume average price for each symbol on a per-minute basis, using the start of the minute as the binning value.

```python skip-test
from deephaven import caf
vwap = trades.view("Sym","Size","Price","TimeBin=lowerBin(Time,1*MINUTE)","GrossPrice=Price*Size")\
    .by(caf.AggCombo(caf.AggAvg("AvgPrice = Price"),\
    caf.AggSum("Volume = Size"),\
    caf.AggSum("TotalGross = GrossPrice")), "Sym","TimeBin")\
    .updateView("VWAP=TotalGross/Volume")
```

:::note

The `relatedQuotes` and `vwap` tables do not work well outside of trading hours, because the before/after hours events lack real timestamps.

:::

### Create a simple plot

Now, we'll create the `aaplVwap` table to limit the data to AAPL events, then plot VWAP vs actual price for each trade event. The query below depends on the `vwap` table created in the previous example:

```python skip-test
from deephaven import Plot
vWap = Plot.plot("VWAP",candle.where("Symbol=`AAPL`"),"Time","VWap")\
    .show()
plotOHLC = Plot.ohlcPlot("MSFT", candle.where("Symbol=`MSFT`"), "Time", "Open", "High", "Low", "Close")\
   .chartTitle("MSFT")\
   .show()
```

## Related documentation

- [Simple Kafka import](https://deephaven.io/core/docs/how-to-guides/kafka-simple/)
- [Kafka introduction](https://deephaven.io/core/docs/conceptual/kafka-in-deephaven/)
- [How to connect to a Kafka stream](https://deephaven.io/core/docs/how-to-guides/kafka-stream/)
- [Kafka basic terminology](https://deephaven.io/core/docs/conceptual/kafka-basic-terms/)
- [consumeToTable](https://deephaven.io/core/docs/reference/data-import-export/Kafka/consumeToTable/)
