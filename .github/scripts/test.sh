#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

docker-compose -f .github/docker-compose-test.yml up -d

while true; do
    STATUS="$(docker inspect --format {{.State.Health.Status}} github_grpc-api_1)"
    echo "Status: '${STATUS}'"
    if [ "${STATUS}" != "starting" ]; then
        break
    fi
    sleep 1
done

STATUS="$(docker inspect --format {{.State.Health.Status}} github_grpc-api_1)"
echo "Final status: '${STATUS}'"

docker-compose -f .github/docker-compose-test.yml down -v

if [ "${STATUS}" != "healthy" ]; then
    exit 1
fi

exit 0
