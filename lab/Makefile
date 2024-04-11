########################################################################
# CS152 Lab 2: Directed Portion
########################################################################

SRC_DIR := .

bmarks = \
	case-1 \
	case-2 \
	case-3 \
	case-4 \
	case-5 \
	case-6 \
	case-7 \
	case-8 \

CC := riscv64-unknown-elf-gcc
CFLAGS := -O2 -std=gnu11 -Wall -specs=htif_nano.specs
RISCV_OBJDUMP := riscv64-unknown-elf-objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.text.init --section=.data

.PHONY: all

COMMON_SRC := $(wildcard $(SRC_DIR)/common/*) 

define compile_template
$(1).riscv: $(wildcard $(SRC_DIR)/$(1)/*) $(COMMON_SRC)
	$(CC) $(CFLAGS) -I$(SRC_DIR)/common $(addprefix -I$(SRC_DIR)/, $(1)) -o $$@ $(wildcard $(SRC_DIR)/$(1)/*.c) $(wildcard $(SRC_DIR)/common/*.c)
endef

$(foreach bmark,$(bmarks),$(eval $(call compile_template,$(bmark))))

bmarks_riscv_bin  = $(addsuffix .riscv,  $(bmarks))
bmarks_riscv_dump = $(addsuffix .riscv.dump, $(bmarks))

$(bmarks_riscv_dump): %.riscv.dump: %.riscv
	$(RISCV_OBJDUMP) $< > $@

all: $(bmarks_riscv_dump)

.PHONY: clean
clean:
	rm -f -- *.riscv *.o *.dump

.SUFFIXES: # Disable built-in suffix rules
