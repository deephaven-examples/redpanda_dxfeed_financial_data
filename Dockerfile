FROM ghcr.io/deephaven/grpc-api
COPY data/app.d /app.d
RUN pip3 install -r /app.d/requirements.txt
FROM ghcr.io/deephaven/web:0.6.0
COPY data/layouts /data/layouts
RUN chown www-data:www-data /data/layouts
