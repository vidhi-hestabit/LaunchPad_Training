#!/bin/bash

LOGFILE="logs/validate.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting validation..." >> $LOGFILE

# Check if src directory exists
if [ ! -d "src" ]; then
  echo "[$TIMESTAMP] ERROR: src/ directory missing!" | tee -a $LOGFILE
  exit 1
fi

# Check if config.json is valid JSON using jq
if ! jq empty config.json 2>/dev/null; then
  echo "[$TIMESTAMP] ERROR: config.json is invalid JSON!" | tee -a $LOGFILE
  exit 1
fi

echo "[$TIMESTAMP] Validation successful!" >> $LOGFILE
exit 0
