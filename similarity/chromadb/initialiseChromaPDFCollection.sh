#!/bin/bash

PORT=8001
HOST=localhost
PYTHON_INIT_FILE=$1

until echo "testing database readiness" | nc "$HOST" "$PORT"
do
    >&2 echo waiting database not ready
	sleep 1
done

echo PDF collection of database will be created or updated
python3 "$PYTHON_INIT_FILE"

echo database ready