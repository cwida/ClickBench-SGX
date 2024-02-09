This repository contains the code to reproduce the ClickHouse benchmark ([ClickBench](https://github.com/ClickHouse/ClickBench)) on Intel SGX 2 using Gramine. We are currently porting only a limited subset of systems. Our scripts reproduce ClickBench with the following modifications:

* **Structural changes**. The benchmark runners are now written in Python, as shell scripts are not entirely compatible with Gramine. 
* **Caching**. Removing caches by invoking the `drop_caches` command is not supported, as it requires superuser access. We manually clear the caches with Python.
* **Data loading**. The setup of the database should not be executed with Gramine-SGX, due to its performance overhead. We therefore split the script into loading the data in an unencrypted manner and then running the ClickBench workload on an already existing database file.

### DuckDB

```shell
./duckdb/setup.sh  # to download and load the data (unencrypted)
make SGX=1
gramine-sgx ./benchmark duckdb/benchmark_duckdb.py
# results are in duckdb/log.txt
./duckdb/test.sh  # to test the correct behaviour
```
