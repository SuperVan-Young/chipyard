#!/bin/bash

BENCHMARK_DIR=$RISCV/riscv64-unknown-elf/share/riscv-tests/benchmarks
# BENCHMARK_RISCVS=$(find "$BENCHMARK_DIR" -type f ! -name "*.dump")
BENCHMARK_RISCVS=(
    "$BENCHMARK_DIR/dhrystone.riscv"
    # "$BENCHMARK_DIR/median.riscv"
    # "$BENCHMARK_DIR/mm.riscv"
    # "$BENCHMARK_DIR/mt-matmul.riscv"
    # "$BENCHMARK_DIR/mt-vvadd.riscv"
    # "$BENCHMARK_DIR/multiply.riscv"
    # "$BENCHMARK_DIR/pmp.riscv"
    # "$BENCHMARK_DIR/qsort.riscv"
    # "$BENCHMARK_DIR/rsort.riscv"
    # "$BENCHMARK_DIR/spmv.riscv"
    # "$BENCHMARK_DIR/towers.riscv"
    # "$BENCHMARK_DIR/vvadd.riscv"
)

CHIPTOP_BUILD_DIR="/root/chipyard/vlsi/build-asap7-commercial/chipyard.harness.TestHarness.TinyRocketConfig-ChipTop"
SIM_RTL_RUNDIR=$CHIPTOP_BUILD_DIR/sim-rtl-rundir
POWER_RTL_RUNDIR=$CHIPTOP_BUILD_DIR/power-rtl-rundir

POWER_REPORT_DIR=$CHIPTOP_BUILD_DIR/power-report-dir
mkdir -p $POWER_REPORT_DIR

tutorial=asap7

# rtl performance & power
for benchmark_riscv in "${BENCHMARK_RISCVS[@]}"; do
    benchmark_name="${benchmark_riscv##*/}"

    # setup redo
    vcs_timestamp="$SIM_RTL_RUNDIR/simv.daidir/.vcs.timestamp"
    if [ -f $vcs_timestamp ]; then
        rm $vcs_timestamp
    fi
    # run sim-rtl
    echo "Running sim-rtl with benchmark $benchmark_riscv"
    make redo-sim-rtl-debug tutorial=$tutorial BINARY=$benchmark_riscv &
    wait $!

    # setup redo
    if [ -d "$POWER_RTL_RUNDIR" ]; then
        rm -r $POWER_RTL_RUNDIR
    fi
    power_sim_rtl_input_json="$CHIPTOP_BUILD_DIR/power-sim-rtl-input.json"
    if [ -f "$power_sim_rtl_input_json" ]; then
        rm $power_sim_rtl_input_json
    fi
    # run power-rtl
    echo "Running power-rtl with benchmark $benchmark_riscv"
    make power-rtl tutorial=$tutorial BINARY=$benchmark_riscv &
    wait $!
    cp "$POWER_RTL_RUNDIR/waveforms.report" "$POWER_REPORT_DIR/$benchmark_name.report"

done

# post-syn area
# make syn tutorial=asap7

# post-syn simulation & power
# make sim-syn tutorial=asap7 BINARY=$RISCV/riscv64-unknown-elf/share/riscv-tests/isa/rv32ui-p-simple
# make sim-syn tutorial=asap7 BINARY=$RISCV/riscv64-unknown-elf/share/riscv-tests/benchmarks/dhrystone.riscv
# make power-syn tutorial=asap7 BINARY=$RISCV/riscv64-unknown-elf/share/riscv-tests/isa/rv32ui-p-simple
# -