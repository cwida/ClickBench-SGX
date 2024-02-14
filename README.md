This repository contains the code to reproduce the ClickHouse benchmark ([ClickBench](https://github.com/ClickHouse/ClickBench)) on Intel SGX 2 using Gramine. We are currently porting only a limited subset of systems. Our scripts reproduce ClickBench with the following modifications:

* **Structural changes**. The benchmark runners are now written in Python, as shell scripts are not entirely compatible with Gramine. This is because Gramine does not support forking processes in the same enclave.
* **Caching**. Removing caches by invoking the `drop_caches` command is not supported, as it requires superuser access. We manually clear the caches with Python.
* **Data loading**. The setup of the database should not be executed with Gramine-SGX, due to its performance overhead. We therefore split the script into loading the data in an encryped manner and then running the ClickBench workload on an already existing database file.

#### Prerequisites for reproducibility:
* Ubuntu 22.04 or 22.10
* Intel Xeon Platinum CPU (or any CPU supporting Secure Guard Extensions)
* The [linux-sgx](https://github.com/intel/linux-sgx) drivers installed
* Gramine with a private key to sign enclaves (see `gramine-sgx-gen-private-key`)
* The relevant Python3 packages to connect to different databases (`duckdb`, `clickhouse_connect`)

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
