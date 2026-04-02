#!/bin/bash

MODE=$1 #simulate send, simula envio
LIMIT=$2 #how much emails want to sender, que tantos emails quieres enviar

if [[ "$MODE" != "simulate" && "$MODE" != "send" ]]; then
	echo "Use: ./run.sh simulate | ./run.sh send [LIMIT]"
	exit 1
fi

echo "Make docker container"
docker build -t automation_csv . > /dev/null

ARGS="-i data"
if [[ "$MODE" == "simulate"]]; then
	ARGS = "$ARGS --simulate"
else
	ARGS="$ARGS --send"
fi

if [[! -z "$LIMIT" ]]; then
	ARGS="$ARGS --limit $LIMIT"
fi

echo "Execute container"
docker run --rm \
    -v $(pwd)/data:/app/data:Z \
    -v $(pwd)/output:/app/output:Z \
    -v $(pwd)/logs:/app/logs:Z \
    automation_csv $ARGS

echo "Process ended, see  output/ y logs/"
