SELECT UserID FROM read_parquet('duckdb-parquet-encrypted/hits.parquet', force_direct_io=true);
