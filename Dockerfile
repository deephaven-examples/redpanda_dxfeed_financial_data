FROM ghcr.io/deephaven/grpc-api AS dx-grpc-api
COPY data/app.d /app.d

FROM ghcr.io/deephaven/web:0.6.0 AS dx-web
COPY data/layouts /data/layouts
RUN chown www-data:www-data /data/layouts

FROM python:3.8 AS dxfeed-publish-all
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_all_tables.py .
CMD [ "python3", "publish_all_tables.py"]

FROM python:3.8 AS dxfeed-publish-trade
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_trade_table.py .
CMD [ "python3", "publish_trade_table.py"]

FROM python:3.8 AS dxfeed-publish-quote
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_quote_table.py .
CMD [ "python3", "publish_quote_table.py"]

FROM python:3.8 AS dxfeed-publish-candle
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_candle_table.py .
CMD [ "python3", "publish_candle_table.py"]

FROM python:3.8 AS dxfeed-publish-profile
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_profile_table.py .
CMD [ "python3", "publish_profile_table.py"]

FROM python:3.8 AS dxfeed-publish-summary
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_summary_table.py .
CMD [ "python3", "publish_summary_table.py"]

FROM python:3.8 AS dxfeed-publish-order
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_order_table.py .
CMD [ "python3", "publish_order_table.py"]

FROM python:3.8 AS dxfeed-publish-underlying
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_underlying_table.py .
CMD [ "python3", "publish_underlying_table.py"]

FROM python:3.8 AS dxfeed-publish-timeandsale
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_timeAndSale_table.py .
CMD [ "python3", "publish_timeAndSale_table.py"]

FROM python:3.8 AS dxfeed-publish-series
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/publish_series_table.py .
CMD [ "python3", "publish_series_table.py"]
