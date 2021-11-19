FROM ghcr.io/deephaven/grpc-api AS dx-grpc-api
COPY data/app.d /app.d

FROM ghcr.io/deephaven/web:0.6.0 AS dx-web
COPY data/layouts /data/layouts
RUN chown www-data:www-data /data/layouts

FROM python:3.8 AS dxfeed-publish
COPY dxfeed/requirements.txt .
RUN pip install -r requirements.txt
COPY dxfeed/fin_pub.py .
CMD [ "python3", "fin_pub.py"]
