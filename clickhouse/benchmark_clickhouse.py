#!/usr/bin/python3

import subprocess
import os

TRIES = 3
QUERY_NUM = 1

queries_file_path = "clickhouse/queries.sql"
result_csv_path = "clickhouse/result.csv"

print("Starting benchmark...")

# check if the log file exists, and delete it if it does
if os.path.exists(result_csv_path):
    os.remove(result_csv_path)

with open(queries_file_path, 'r') as queries_file, open(result_csv_path, 'w') as result_csv:
    for query in queries_file:
        print(f"\nRunning query: {query.strip()}")
        # Clear caches if FQDN is not set
        # if 'FQDN' not in os.environ:
            #subprocess.run(['sync'])
            #subprocess.run(['echo', '3', '|', 'sudo', 'tee', '/proc/sys/vm/drop_caches', '>/dev/null'], shell=True)

        print("[", end="")
        for i in range(1, TRIES + 1):
            command = ' '.join(['clickhouse-client', '--time', '--format=Null', '--query "', query.strip(), '" --progress', '0'])

            # Run the command using subprocess.run
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)  # Add shell=True when using a command string
            # Print result or "null" if there was an error
            # The original script redirects stderr to stdout, we just use stderr
            print(f'"{result.stderr.strip()}"' if result.returncode == 0 else "null", end="")

            # Write result to result.csv
            result_csv.write(f"{QUERY_NUM},{i},{result.stderr.strip()}\n")

            if i != TRIES:
                print(", ", end="")

        print("],")
        QUERY_NUM += 1

print("\nBenchmark completed. See results in clickhouse/result.csv for query timings.")
