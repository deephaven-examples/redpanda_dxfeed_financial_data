docker build --target dx-server -t redpanda-dxfeed-financial-data/dx-server .
docker build --target dx-web -t redpanda-dxfeed-financial-data/dx-web:latest .
#docker build --target dxfeed-publish-all -t redpanda-dxfeed-financial-data/dxfeed-publish-all:latest .
docker build --target dxfeed-publish-trade -t redpanda-dxfeed-financial-data/dxfeed-publish-trade:latest .
docker build --target dxfeed-publish-quote -t redpanda-dxfeed-financial-data/dxfeed-publish-quote:latest .
docker build --target dxfeed-publish-candle -t redpanda-dxfeed-financial-data/dxfeed-publish-candle:latest .
docker build --target dxfeed-publish-profile -t redpanda-dxfeed-financial-data/dxfeed-publish-profile:latest .
docker build --target dxfeed-publish-summary -t redpanda-dxfeed-financial-data/dxfeed-publish-summary:latest .
docker build --target dxfeed-publish-order -t redpanda-dxfeed-financial-data/dxfeed-publish-order:latest .
docker build --target dxfeed-publish-underlying -t redpanda-dxfeed-financial-data/dxfeed-publish-underlying:latest .
docker build --target dxfeed-publish-timeandsale -t redpanda-dxfeed-financial-data/dxfeed-publish-timeandsale:latest .
docker build --target dxfeed-publish-series -t redpanda-dxfeed-financial-data/dxfeed-publish-series:latest .
docker-compose up -d
