#!/usr/bin/python3

import os
import duckdb
import timeit
import sys
import time

def run_query(query, log_file):
    with open(log_file, 'a') as log:

        print(f"\nRunning query: {query.strip()}")
        log.write(query + '\n')

        con = duckdb.connect()
        con.execute("PRAGMA add_parquet_key('key128', '0123456789112345')");
        for try_num in range(3):
            start = timeit.default_timer()
            results = con.sql(query).fetchall()
            end = timeit.default_timer()
            log.write(str(end - start) + '\n')
            print(f"Query finished in {end - start:.6f} seconds")
            del results

def main():
    query_file_path = os.path.join(os.getcwd(), "duckdb/explain_query.sql")
    output_log_path = os.path.join(os.getcwd(), "duckdb-parquet-encrypted/log.txt")

    print("Starting benchmark...")

    with open(query_file_path, 'r') as queries_file:
        for query in queries_file:
            run_query(query.strip(), output_log_path)

    print("\nBenchmark finished. Check duckdb-parquet-encrypted/log.txt for the query timings.")

if __name__ == "__main__":
    main()
