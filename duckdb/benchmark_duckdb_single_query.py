#!/usr/bin/python3

import os
import duckdb
import timeit
import sys
import subprocess

def run_query(query, log_file, query_path):

    if os.path.exists(query_path):
        os.remove(query_path)
        
    with open(query_path, 'a') as query_file:  
        query_file.write(query + '\n')
    
    subprocess.run("sudo sync; sudo sh -c 'echo 3 >/proc/sys/vm/drop_caches'", shell=True, check=True)
    print("\nStarting enclave...")
    subprocess.run("numactl --cpunodebind=0 --membind=0 gramine-sgx benchmark duckdb/enclave_query.py", shell=True, check=True)
    print("Enclave terminated...")

def main():
    queries_file_path = os.path.join(os.getcwd(), "duckdb-parquet-encrypted/queries.sql")
    output_log_path = os.path.join(os.getcwd(), "duckdb-parquet-encrypted/log.txt")
    single_query_path = os.path.join(os.getcwd(), "duckdb/explain_query.sql")

    print("Starting benchmark...")

    # check if the log file exists, and delete it if it does
    if os.path.exists(output_log_path):
        os.remove(output_log_path)

    with open(queries_file_path, 'r') as queries_file:
        for query in queries_file:
            run_query(query.strip(), output_log_path, single_query_path)

    print("\nBenchmark finished. Check duckdb-parquet-encrypted/log.txt for the query timings.")

if __name__ == "__main__":
    main()
