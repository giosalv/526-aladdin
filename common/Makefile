
.PHONY: all clean
ifdef ORIG_ALADDIN
EXE_SRC = aladdin
EXE = aladdin
else
EXE_SRC = aladdin
EXE = aladdin-generalized
CFLAGS += -DGENERALIZED_TRACE
endif

MACHINE_MODEL_OBJS = BaseDatapath.o ScratchpadDatapath.o Scratchpad.o \
                     Registers.o Partition.o LogicalArray.o ReadyPartition.o \
                     SourceManager.o
UTILS_OBJS = file_func.o generic_func.o power_func.o opcode_func.o
DDDG_OBJS = DDDG.o
OBJS += $(MACHINE_MODEL_OBJS) $(UTILS_OBJS) $(DDDG_OBJS)
OBJ_FILES = $(patsubst %.o,obj/%.o,$(OBJS))

OBJ_DIR = obj

CACTI_DIR = cacti-p
CACTI_OBJ_DIR = $(CACTI_DIR)/obj_opt

ifndef NTHREADS
  NTHREADS = 8
endif
CACTI_OBJS = Ucache.o bank.o cacti_interface.o decoder.o  parameter.o \
             technology.o arbiter.o  basic_circuit.o  component.o  htree2.o \
						 mat.o router.o uca.o area.o crossbar.o io.o nuca.o subarray.o \
						 wire.o powergating.o
CACTI_SRCS = $(patsubst %.o,%.cc,$(CACTI_OBJS))
CACTI_OBJ_FILES = $(patsubst %.o,$(CACTI_OBJ_DIR)/%.o,$(CACTI_OBJS))

DEBUG = -DDEBUG
#DEBUG =
CFLAGS += $(DEBUG) $(BITWIDTH) -g -O0 -std=c++0x -I$(BOOST_ROOT) -Icacti-p
LFLAGS += -lz -L$(BOOST_ROOT)/stage/lib -lboost_graph -lboost_regex -lpthread


all : $(EXE)

obj_dir:
	mkdir -p $(OBJ_DIR)
	mkdir -p $(CACTI_OBJ_DIR)

lib : obj_dir $(OBJ_FILES) $(CACTI_OBJ_FILES)
	ar rcs $(ALADDIN_HOME)/libaladdin.a $(OBJ_FILES) $(CACTI_OBJ_FILES)

$(EXE): obj_dir $(CACTI_OBJ_FILES) $(OBJ_FILES)
	$(CXX) $(CFLAGS) -c aladdin.cpp
	$(CXX)  $(BITWIDTH) -o $(EXE) $(EXE_SRC).o $(OBJ_FILES) $(CACTI_OBJ_FILES) $(LFLAGS)

$(OBJ_DIR)/%.o : %.h %.cpp
	$(CXX) $(CFLAGS) -o $@ -c $*.cpp

$(CACTI_OBJ_DIR)/%.o : $(CACTI_DIR)/%.cc
	$(CXX) $(CFLAGS)  -DNTHREADS=$(NTHREADS) -o $@ -c $(CACTI_DIR)/$*.cc

clean:
	rm -f $(OBJ_DIR)/*.o
	rm -f $(CACTI_OBJ_DIR)/*.o
	rm -f aladdin
	rm -f aladdin-generalized

