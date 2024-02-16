#!/bin/bash

# Install
cd clickhouse

if test -f clickhouse; then
    # ClickHouse is already installed. Do nothing.
    :
else
    curl https://clickhouse.com/ | sh
    sudo ./clickhouse install --noninteractive
fi

# Skipping the higher compression installation

sudo clickhouse start

while true
do
    clickhouse-client --query "SELECT 1" && break
    sleep 1
done

# Load the data

clickhouse-client < create.sql

if test -f hits.parquet; then
    :
else
    wget --no-verbose --continue 'https://datasets.clickhouse.com/hits_compatible/hits.parquet'
fi
