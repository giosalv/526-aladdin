SRCS=hello.c

ACCEL_NAME = hello
TEST_BIN = $(ACCEL_NAME)
export TRACE_OUTPUT_DIR=$(ACCEL_NAME)
ifndef WORKLOAD
  export WORKLOAD=main
endif
include ../common/Makefile.common
include ../common/Makefile.tracer
