#!/bin/bash
# run.sh - Run Automation CSV on Linux / Mac
# Usage: ./run.sh [simulate|send] [LIMIT]

MODE=$1       # simulate or send
LIMIT=$2      # number of emails to send (optional)

# Default to simulate if no mode provided
if [[ -z "$MODE" ]]; then
    MODE="simulate"
fi

if [[ "$MODE" != "simulate" && "$MODE" != "send" ]]; then
    echo "Usage: ./run.sh [simulate|send] [LIMIT]"
    exit 1
fi

echo "Building Docker container..."
docker build -t automation_csv . > /dev/null

ARGS="-i data"
if [[ "$MODE" == "simulate" ]]; then
    ARGS="$ARGS --simulate"
else
    ARGS="$ARGS --send"
fi

if [[ ! -z "$LIMIT" ]]; then
    ARGS="$ARGS --limit $LIMIT"
fi

echo "Executing container..."
docker run --rm \
    -v "$(pwd)/data:/app/data:Z" \
    -v "$(pwd)/output:/app/output:Z" \
    -v "$(pwd)/logs:/app/logs:Z" \
    automation_csv $ARGS

echo "Process finished! Check 'output/' and 'logs/' folders."
