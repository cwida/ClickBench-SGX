#!/bin/bash

# Install

sudo apt-get update
sudo apt-get install -y python3-pip
pip install duckdb psutil

# Load the data

if test -f duckdb-parquet/hits.parquet; then
    :
else
    wget --no-verbose --continue 'https://datasets.clickhouse.com/hits_compatible/hits.parquet' -P duckdb
fi

./duckdb/load.py
