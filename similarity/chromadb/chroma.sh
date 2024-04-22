#!/bin/bash

PORT=$2
HOST=$1

if [[ ! $# == 2 ]]; 
then
    PORT=8000
    HOST=localhost
fi

export ANONYMIZED_TELEMETRY=False && chroma run --host "$HOST" --port "$PORT"

exit 0