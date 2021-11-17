pip install confluent_kafka
pip install dxfeed
docker build --tag deephaven-examples/redpanda_dxfeed_financial_data-grpc-api .
docker-compose up -d
python3 data/app.d/fin_pub.py
