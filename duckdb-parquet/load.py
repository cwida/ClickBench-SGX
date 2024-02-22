#!/usr/bin/env python3

import duckdb
import timeit
import psutil

con = duckdb.connect(database="duckdb-parquet/my-db.duckdb", read_only=False)

# enable the progress bar
con.execute('PRAGMA enable_progress_bar')
con.execute('PRAGMA enable_print_progress_bar;')
# disable preservation of insertion order
con.execute("SET preserve_insertion_order=false")

# perform the actual load
print("Will load the data")
start = timeit.default_timer()
con.execute(open("duckdb-parquet/create.sql").read())
end = timeit.default_timer()
print(end - start)
