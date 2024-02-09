#!/bin/bash

#/usr/bin/cat /home/ubuntu/ClickHouse-SGX/ClickBench/duckdb/queries.sql | while read query; do
    #/usr/bin/dd if=/dev/zero of=/tmp/testfile bs=2G count=1

#    /home/ubuntu/ClickHouse-SGX/ClickBench/duckdb/query.py <<< "${query}"
#done

# Read the first line from queries.sql using head
#query=$(/usr/bin/head -n 1 /home/ubuntu/ClickHouse-SGX/ClickBench/duckdb/queries.sql)
#/home/ubuntu/ClickHouse-SGX/ClickBench/duckdb/query.py <<< "${query}"
while IFS= read -r query; do
    /home/ubuntu/ClickHouse-SGX/ClickBench/duckdb/query.py <<< "${query}"
done < "/home/ubuntu/ClickHouse-SGX/ClickBench/duckdb/queries.sql"
