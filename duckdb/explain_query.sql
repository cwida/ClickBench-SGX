SELECT * FROM read_parquet('duckdb-parquet-encrypted/hits_encrypted.parquet', encryption_config={footer_key: 'key128'}) WHERE URL LIKE '%google%' ORDER BY EventTime LIMIT 10;
