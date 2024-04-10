########################################################################
# CS152 Lab 2: Directed Portion
########################################################################

SRC_DIR := .

bmarks = \
	transpose \

CC := riscv64-unknown-elf-gcc
CFLAGS := -O2 -std=gnu11 -Wall -specs=htif_nano.specs
INCS  += -I$(SRC_DIR)/common $(addprefix -I$(SRC_DIR)/, $(bmarks))

.PHONY: all

COMMON_SRC := $(wildcard $(SRC_DIR)/common/*) 

define compile_template
$(1).riscv: $(wildcard $(SRC_DIR)/$(1)/*) $(COMMON_SRC)
	$(CC) $(INCS) $(CFLAGS) -o $$@ $(wildcard $(SRC_DIR)/$(1)/*.c) $(wildcard $(SRC_DIR)/common/*.c) $(wildcard $(SRC_DIR)/common/*.h)
endef

$(foreach bmark,$(bmarks),$(eval $(call compile_template,$(bmark))))

bmarks_riscv_bin  = $(addsuffix .riscv,  $(bmarks))

all: bmarks_riscv_bin

.PHONY: clean
clean:
	rm -f -- *.riscv *.o *.dump

.SUFFIXES: # Disable built-in suffix rules
