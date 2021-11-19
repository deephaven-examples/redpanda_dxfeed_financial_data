docker build --target dx-grpc-api -t redpanda-dxfeed-financial-data/dx-grpc-api .
docker build --target dx-web -t redpanda-dxfeed-financial-data/dx-web:latest .
docker build --target dxFeed-publish -t redpanda-dxfeed-financial-data/dxfeed-publish:latest .
docker-compose up -d
