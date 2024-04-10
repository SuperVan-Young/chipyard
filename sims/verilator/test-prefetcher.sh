#!/bin/bash

CONFIG=${1:-"CS152RocketNoPrefetchConfig"}

CHIPYARD_ROOT=$(cd "$(dirname "$0")/../../" && pwd)

source ${CHIPYARD_ROOT}/env.sh

# make sure the simulator is built
if [ ! -f "${CHIPYARD_ROOT}/sims/verilator/simulator-chipyard.harness-${CONFIG}" ]; then
    echo "Building simulator for ${CONFIG}"
    make CONFIG=${CONFIG}
fi

# run simulation in parallel
bmarks=(
	case-1 \
	case-2 \
	case-3 \
	case-4 \
	case-5 \
	case-6 \
	case-7 \
	case-8 
)

for bmark in "${bmarks[@]}"
do
    echo "Running $bmark"
    make run-binary CONFIG=${CONFIG} BINARY=${CHIPYARD_ROOT}/lab/${bmark}.riscv &
done

wait