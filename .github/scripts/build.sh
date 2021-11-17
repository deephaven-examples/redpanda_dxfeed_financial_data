#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

docker build --tag deephaven-examples/redpanda_dxfeed_financial_data-grpc-api .
