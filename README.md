# redpanda_dxfeed_financial_data

This repository publishes [dxFeed](https://dxfeed.com/) demo data to a Kafka [Redpanda](https://vectorized.io/) to stream. The Kafka stream is then consumed into Deephaven. Running `redpanda_start.sh` will create stock market tables on [http://localhost:10000/ide](http://localhost:10000/ide). Note that the Deephaven's default authentication (pre-shared key). For more information on using pre-shared key authentication and setting your own key, see [How to configure and use pre-shared key authentication](https://deephaven.io/core/docs/how-to-guides/authentication/auth-psk/).

## How it works

### Deephaven application mode

This app runs using [Deephaven's application mode](https://deephaven.io/core/docs/how-to-guides/app-mode/).

### Components

* `Dockerfile` - The dockerfile for the application. This extends the default Deephaven images to add dependencies. See our guide, [How to install Python packages](https://deephaven.io/core/docs/how-to-guides/install-python-packages/#add-packages-to-a-custom-docker-image), for more information.
* `docker-compose.yml` - The Docker Compose file for the application. This is mostly the same as the [Deephaven docker-compose file](https://raw.githubusercontent.com/deephaven/deephaven-core/main/containers/python-examples/docker-compose.yml) with modifications to run Redpanda, application mode,  dxFeed Kafka producer and the custom dependencies.
* `redpanda_start.sh` - A simple helper script to launch the application.
* `data/app.d/start.app` - The Deephaven application mode app file.
* `data/app.d/tables.py` - The Deephaven queries to initialize tables.
* `data/layouts/layout.json` - The Deephaven layout to show all initialized tables.
* `data/notebooks/query.py` - A Deephaven sample query to run on tables.
* `dxfeed/requirements.txt` - Python dependencies for the application.
* `dxfeed/fin_pub.py` - The Python script that pulls the data from [dxFeed](https://dxfeed.com/) and streams to [Redpanda](https://vectorized.io/).


### High level overview

The demo feed contains a handful of symbols with 15 minute delayed publication during trading hours. In order to provide events during non-trading hours, the demo feed will replay random old events every few seconds.

The Repanda Kafka producer used in this guide creates the following Deephaven tables:

- `trade`: Last Sale price for a given instrument + daily volume
- `quote`: Bid/Ask prices for a given instrument
- `candle`: Charting OHLCV candle
- `profile`: Instrument profile
- `summary`: Open-High-Low-Close values for current day and Close for previous trading day
- `order`: Market depth: Level 2 quote by market maker /regional exchange quote /element of order book
- `underlying`: Snapshot of computed values that are available for an option underlying symbol based on the option prices on the market
- `timeAndSale`: Trade in a tape of trades for a given instrument
- `series`: Snapshot of computed values that are available for option series for a given underlying symbol based on the option prices on the market


With the instrument:

```python
symbols = ['SPY', 'AAPL', 'IBM', 'MSFT', 'DIA', 'XLF', 'GOOG', 'AMZN', 'TSLA', 'SPX', 'HPQ', 'CSCO', 'INTC', 'AXP']
```

## Dependencies

* The [Deephaven-core dependencies](https://github.com/deephaven/deephaven-core#required-dependencies) are required to build and run this project.

## Launch

To launch the latest release, you can clone the repository via:

```shell
git clone https://github.com/deephaven-examples/redpanda-dxfeed-financial-data.git
cd redpanda-dxfeed-financial-data
```

A start script will install the needed python modules. It will also start the Deephaven IDE, Redpanda images and execute the python application to produce the stream from dxFeed.

To run it, execute:

```shell
./redpanda_start.sh
```

Running this script will start several Docker containers that work together to pull data from dxFeed, publish that to various Kafka topics and then are consumed by Deephaven. To view the data navigate to [http://localhost:10000/ide](http://localhost:10000/ide).  To view the tables you might need to refresh the page by going in the top right **Panels** tab and clicking the circular refresh button.

Tables and sample query will appear in the IDE.

### Use the data

We can then write other queries which combine and/or aggregate data from these streams. This query uses an [as-of join](https://deephaven.io/core/docs/reference/table-operations/join/aj/) to correlate trade events with the most recent bid for the same symbol. A sample query is provided, edit this query write your own! Visit [https://deephaven.io/](https://deephaven.io/) to learn more!

:::note

Some tables only work during trading hours, because the before/after hours events lack real timestamps.  This data is demo data, it is provided here for demonstrative use without any warranty as to the accuracy, reliability, or completeness of the data.

:::

## Related documentation

- [Simple Kafka import](https://deephaven.io/core/docs/how-to-guides/kafka-simple/)
- [Kafka introduction](https://deephaven.io/core/docs/conceptual/kafka-in-deephaven/)
- [How to connect to a Kafka stream](https://deephaven.io/core/docs/how-to-guides/kafka-stream/)
- [Kafka basic terminology](https://deephaven.io/core/docs/conceptual/kafka-basic-terms/)
- [consumeToTable](https://deephaven.io/core/docs/reference/data-import-export/Kafka/consumeToTable/)
