clickhouse-client --query "SELECT total_bytes FROM system.tables WHERE name = 'hits_encrypted' AND database = 'default'"
sudo clickhouse stop
