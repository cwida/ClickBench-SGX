#!/bin/bash

# Install

sudo apt-get update
sudo apt-get install -y python3-pip
pip install duckdb psutil

# Load the data

if test duckdb/hits.csv; then
    :
else
    wget --no-verbose --continue 'https://datasets.clickhouse.com/hits_compatible/hits.csv.gz' -P duckdb
    gzip -d duckdb/hits.csv.gz
fi

./duckdb/load.py
# 414 seconds
