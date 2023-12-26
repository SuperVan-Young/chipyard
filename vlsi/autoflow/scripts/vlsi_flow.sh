#!/bin/bash --login
source ~/.bashrc

CHIPYARD_ROOT='/home/chenhao.xue/chipyard'
cd $CHIPYARD_ROOT
source env.sh
cd $CHIPYARD_ROOT/vlsi

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <BOOM Config Index>"
    exit 1
fi
BOOM_CFG_IDX=$1
BOOM_CFG_NAME="Boom${BOOM_CFG_IDX}Config"

echo $BOOM_CFG_NAME
exit 1

make buildfile CONFIG=$BOOM_CFG_NAME
make redo-syn CONFIG=$BOOM_CFG_NAME

# performance of dhrystone
make redo-sim-rtl-debug CONFIG=$BOOM_CFG_NAME BINARY=$RISCV/riscv64-unknown-elf/share/riscv-tests/benchmarks/dhrystone.riscv &
wait

# power of simple testcase
make redo-sim-rtl-debug CONFIG=$BOOM_CFG_NAME BINARY=$RISCV/riscv64-unknown-elf/share/riscv-tests/isa/rv32ui-p-simple &
wait

if [ -f "/root/chipyard/vlsi/build/chipyard.harness.TestHarness.N${1}BoomConfig-ChipTop/power-sim-rtl-input.json" ]; then
    make redo-power-rtl CONFIG=$BOOM_CFG_NAME BINARY=$RISCV/riscv64-unknown-elf/share/riscv-tests/isa/rv32ui-p-simple &
    wait
else
    make power-rtl CONFIG=$BOOM_CFG_NAME BINARY=$RISCV/riscv64-unknown-elf/share/riscv-tests/isa/rv32ui-p-simple &
    wait
fi
