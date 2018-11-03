#!/usr/bin/env bash

set -o nounset

MOCKSI_HOST=${MOCKSI_HOST:=localhost}
MOCKSI_PORT=${MOCKSI_PORT:=9090}
TEST_FILE=${TEST_FILE:=test_load.py}
CLIENTS=${CLIENTS:=10}
RATE=${RATE:=1}
TIME_LIMIT=${TIME_LIMIT:=30s}

locust -f "$TEST_FILE" -c "$CLIENTS" -r "$RATE" -t "$TIME_LIMIT" --no-web --host=http://"$MOCKSI_HOST":"$MOCKSI_PORT"