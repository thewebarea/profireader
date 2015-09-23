#!/bin/bash

source .venv/bin/activate
while [[ True ]]; do
    python run.py --host=$1 --port=$2 >> /var/log/profi-$1.log 2>&1
    sleep 5
done
