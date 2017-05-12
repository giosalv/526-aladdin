SRCS=pagerank.c

ACCEL_NAME = pagerank
TEST_BIN = $(ACCEL_NAME)
export TRACE_OUTPUT_DIR=$(ACCEL_NAME)
ifndef WORKLOAD
  export WORKLOAD=pagerank1,pagerank2
endif
include ../common/Makefile.common
include ../common/Makefile.tracer
