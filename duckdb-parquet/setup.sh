#!/bin/bash

# Install

sudo apt-get update
sudo apt-get install -y python3-pip
pip install duckdb psutil

# Load the data

test -e duckdb-parquet/hits.parquet || wget --no-verbose --continue 'https://datasets.clickhouse.com/hits_compatible/hits.parquet' -P duckdb-parquet

./duckdb-parquet/load.py
