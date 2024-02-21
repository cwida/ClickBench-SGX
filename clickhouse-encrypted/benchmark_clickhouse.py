#!/usr/bin/python3

import os
import clickhouse_connect
import timeit
import sys

def run_query(query, log_file):
    with open(log_file, 'a') as log:
        print(f"\nRunning query: {query.strip()}")
        log.write(query + '\n')

        client = clickhouse_connect.get_client(host='localhost', username='default')
        for try_num in range(3):
            start = timeit.default_timer()
            results = client.command(query)
            end = timeit.default_timer()
            log.write(str(end - start) + '\n')
            print(f"Query finished in {end - start:.6f} seconds")
            del results

def main():
    queries_file_path = "clickhouse-encrypted/queries.sql"
    result_csv_path = "clickhouse-encrypted/result.csv"

    print("Starting benchmark...")

    # check if the log file exists, and delete it if it does
    if os.path.exists(result_csv_path):
        os.remove(result_csv_path)

    with open(queries_file_path, 'r') as queries_file:
        for query in queries_file:
            run_query(query.strip(), result_csv_path)

    print("\nBenchmark completed. See results in clickhouse-encrypted/result.csv for query timings.")

if __name__ == "__main__":
    main()
