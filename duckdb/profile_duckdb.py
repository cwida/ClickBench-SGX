#!/usr/bin/python3

import os
import duckdb
import timeit

def run_query(query):
    print(f"\nRunning query: {query.strip()}")

    con = duckdb.connect(database="duckdb/my-db.duckdb", read_only=False)
    con.execute("PRAGMA enable_profiling")
    con.execute("PRAGMA add_parquet_key('key128', '0123456789112345')")
    
    for try_num in range(3):
        start = timeit.default_timer()
        con.sql(query).explain("analyze")
        end = timeit.default_timer()
        print(f"Query finished in {end - start:.6f} seconds")

def main():
    queries_file_path = os.path.join(os.getcwd(), "duckdb/explain_query.sql")
    print("Starting benchmark...")

    with open(queries_file_path, 'r') as queries_file:
        for query in queries_file:
            run_query(query.strip())

    print("\nBenchmark finished. Check duckdb/explain.txt for the query timings.")

if __name__ == "__main__":
    main()
