SELECT RegionID, COUNT(DISTINCT UserID) AS u FROM read_parquet('duckdb-parquet-encrypted/hits_encrypted.parquet', encryption_config={footer_key: 'key128'}) GROUP BY RegionID ORDER BY u DESC LIMIT 10;
