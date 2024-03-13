#!/usr/bin/python3

import os
import duckdb
import timeit

def run_query(query, explain_file):
    with open(explain_file, 'a') as log:
        print(f"\nRunning query: {query.strip()}", flush=True)
        log.write(query + '\n')

        con = duckdb.connect(database="duckdb/my-db.duckdb", read_only=False)
        con.execute("PRAGMA enable_profiling")
        con.execute("SET memory_limit = '64GB';")
        #con.execute("SET threads TO 1;")
        #con.execute("SET threads TO 16;")
        #con.execute("SET threads TO 32;")
        con.execute("PRAGMA add_parquet_key('key128', '0123456789112345')")
        
        for try_num in range(3):
            start = timeit.default_timer()
            con.sql(query).explain("analyze")
            end = timeit.default_timer()
            log.write(str(end - start) + '\n')
            print(f"Query finished in {end - start:.6f} seconds", flush=True)

def main():
    queries_file_path = os.path.join(os.getcwd(), "duckdb/explain_query.sql")
    explain_file_path = os.path.join(os.getcwd(), "duckdb/explain.txt")
    print("Starting benchmark...", flush=True)

    if os.path.exists(explain_file_path):
        os.remove(explain_file_path)

    with open(queries_file_path, 'r') as queries_file:
        for query in queries_file:
            run_query(query.strip(), explain_file_path)

    print("\nBenchmark finished. Check duckdb/explain.txt for the query timings.", flush=True)

if __name__ == "__main__":
    main()
