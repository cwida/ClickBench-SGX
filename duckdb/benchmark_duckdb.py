#!/usr/bin/python3

import os
import duckdb
import timeit
import sys

def run_query(query, log_file):
    with open(log_file, 'a') as log:
        print(f"\nRunning query: {query.strip()}")
        log.write(query + '\n')

        con = duckdb.connect(database="duckdb/my-db.duckdb", read_only=False)
        con.sql("SET threads TO 16").fetchall()
        for try_num in range(3):
            start = timeit.default_timer()
            results = con.sql(query).fetchall()
            end = timeit.default_timer()
            log.write(str(end - start) + '\n')
            print(f"Query finished in {end - start:.6f} seconds")
            del results

def main():
    queries_file_path = os.path.join(os.getcwd(), "duckdb/queries.sql")
    output_log_path = os.path.join(os.getcwd(), "duckdb/log.txt")

    print("Starting benchmark...")

    # check if the log file exists, and delete it if it does
    if os.path.exists(output_log_path):
        os.remove(output_log_path)

    with open(queries_file_path, 'r') as queries_file:
        for query in queries_file:
            run_query(query.strip(), output_log_path)

    print("\nBenchmark finished. Check duckdb/log.txt for the query timings.")

if __name__ == "__main__":
    main()
