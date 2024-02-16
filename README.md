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

### ClickHouse (encrypted)
Firstly, we need to set up the server using encrypted storage (inspired by [this blog post](https://kb.altinity.com/altinity-kb-setup-and-maintenance/disk_encryption/)). This is made by overriding the default configuration, allocating a folder for the encrypted files. We assume a fresh ClickHouse installation, with default parameters and paths. In order to create the user `clickhouse`, ClickHouse should be already installed. We, therefore, advise to run the benchmark in an unencrypted way first, or install ClickHouse before running the benchmarks:
```shell
cd clickhouse
curl https://clickhouse.com/ | sh
sudo ./clickhouse install --noninteractive
sudo clickhouse start
sudo clickhouse stop
cd ..
```
Now, the encrypted disk can be created.
```shell
$ mkdir -p /data/clickhouse_encrypted
$ chown clickhouse.clickhouse /data/clickhouse_encrypted
$ cp clickhouse/encrypted_storage.xml /etc/clickhouse-server/config.d/encrypted_storage.xml
```
The server starts by running the setup script, and then benchmarks can be executed.
```shell
./clickhouse/setup.sh  # to download and load the data (encrypted)
make SGX=1
gramine-sgx ./benchmark clickhouse/benchmark_clickhouse.py
# results are in clickhouse/result.csv
./clickhouse/test.sh  # to test the correct behaviour and stop the server
```
