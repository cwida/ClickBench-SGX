#!/bin/bash

# Install

sudo apt-get update
sudo apt-get install -y python3-pip
pip install duckdb psutil

# Load the data

test -f duckdb/hits.csv || (wget --no-verbose --continue 'https://datasets.clickhouse.com/hits_compatible/hits.csv.gz' -P duckdb && gzip -d duckdb/hits.csv.gz)

./duckdb/load.py
# 414 seconds
