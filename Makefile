ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: benchmark.manifest clickhouse.manifest
ifeq ($(SGX),1)
all: benchmark.manifest.sgx benchmark.sig clickhouse.manifest.sgx clickhouse.sig
endif

benchmark.manifest: benchmark.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		-Dexecdir=$(shell pwd) \
		-Dentrypoint=$(realpath $(shell sh -c "command -v python3")) \
		$< > $@

clickhouse.manifest: clickhouse.manifest.template
	gramine-manifest \
                -Dlog_level=$(GRAMINE_LOG_LEVEL) \
                -Darch_libdir=$(ARCH_LIBDIR) \
                -Dexecdir=$(shell pwd) \
                $< > $@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# for details on this workaround see
# https://github.com/gramineproject/gramine/blob/e8735ea06c/CI-Examples/helloworld/Makefile
benchmark.manifest.sgx benchmark.sig: sgx_sign_benchmark
	@:

clickhouse.manifest.sgx clickhouse.sig: sgx_sign_clickhouse
        @:

.INTERMEDIATE: sgx_sign_benchmark
sgx_sign_benchmark: benchmark.manifest
	gramine-sgx-sign \
		--manifest $< \
		--output $<.sgx

.INTERMEDIATE: sgx_sign_clickhouse
sgx_sign_clickhouse: clickhouse.manifest
	gramine-sgx-sign \
                --manifest $< \
                --output $<.sgx

ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

.PHONY: clean
clean:
	$(RM) *.token *.sig *.manifest.sgx *.manifest

.PHONY: distclean
distclean: clean
	$(RM) *.pt result.txt
