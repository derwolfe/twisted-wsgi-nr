#!/usr/bin/env bash

docker kill twisted-wsgi-nr
docker rm twisted-wsgi-nr
docker build -t twisted-wsgi-nr .
docker run -p 8713:8713 -d \
       -e NEW_RELIC_DEVELOPER_MODE="true" \
       -e NEW_RELIC_LICENSE_KEY="NEWRELICLICENSEKEY" \
       -e NEW_RELIC_APP_NAME="twisted-wsgi-nr" \
       -e NEW_RELIC_LOG="stdout" \
       -e NEW_RELIC_LOG_LEVEL="info" \
       --name twisted-wsgi-nr \
       twisted-wsgi-nr
docker logs -f twisted-wsgi-nr
