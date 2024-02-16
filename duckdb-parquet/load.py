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
con.execute("COPY hits FROM 'duckdb-parquet/hits.parquet'")
con.execute("PRAGMA add_parquet_key('key128', '0123456789112345'");
print("Will export the encrypted data")
con.execute("COPY hits TO 'hits_encrypted.parquet' (ENCRYPTION_CONFIG {footer_key: 'key128'})")
end = timeit.default_timer()
print(end - start)
