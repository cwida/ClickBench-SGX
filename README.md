This repository contains the code to reproduce the ClickHouse benchmark ([ClickBench](https://github.com/ClickHouse/ClickBench)) on Intel SGX 2 using Gramine. We are currently porting only a limited subset of systems. Our scripts reproduce ClickBench with the following modifications:

* **Structural changes**. The benchmark runners are now written in Python, as shell scripts are not entirely compatible with Gramine. 
* **Caching**. Removing caches by invoking the `drop_caches` command is not supported, as it requires superuser access. We manually clear the caches with Python.
* **Data loading**. The setup of the database should not be executed with Gramine-SGX, due to its performance overhead. We therefore split the script into loading the data in an unencrypted manner and then running the ClickBench workload on an already existing database file.

We implement a single manifest file to run all the benchmarks. We assume all the scripts to be called from the parent folder. We recommend the execution of the benchmarking suit in a Python virtual environment.
```shell
python3 -m venv path/to/venv
source path/to/venv/bin/activate
```

### DuckDB

```shell
./duckdb/setup.sh  # to download and load the data (unencrypted)
make SGX=1
gramine-sgx ./benchmark duckdb/benchmark_duckdb.py
# results are in duckdb/log.txt
./duckdb/test.sh  # to test the correct behaviour
```

### ClickHouse
Firstly, we need to set up the server using encrypted storage.
```shell
$ mkdir -p /data/clickhouse_encrypted
$ chown clickhouse.clickhouse /data/clickhouse_encrypted
$ cp clickhouse/encrypted_storage.xml /etc/clickhouse-server/config.d/encrypted_storage.xml
```
The server starts by running the setup script.
