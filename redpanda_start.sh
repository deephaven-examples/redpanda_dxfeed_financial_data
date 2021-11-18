docker build --target dx-grpc-api -t redpanda_dxfeed_financial_data/dx-grpc-api .
docker build --target dx-web -t redpanda_dxfeed_financial_data/dx-web:latest .
docker build --target dxFeed_publish -t redpanda_dxfeed_financial_data/dxfeed_publish:latest .
docker-compose up -d
