#!/bin/bash

# Install
cd clickhouse

if test clickhouse; then
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

if test hits.tsv; then
    :
else
    wget --no-verbose --continue 'https://datasets.clickhouse.com/hits_compatible/hits.tsv.gz'
    gzip -d hits.tsv.gz
fi

clickhouse-client --time --query "INSERT INTO hits FORMAT TSV" < hits.tsv

