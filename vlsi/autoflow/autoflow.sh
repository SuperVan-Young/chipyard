#!/bin/bash --login
source ~/.bashrc

CHIPYARD_ROOT='/home/chenhao.xue/chipyard'
cd $CHIPYARD_ROOT
source env.sh
cd $CHIPYARD_ROOT/vlsi


# run the following synthesis flow automatically
while true; do

    BOOM_CFG_IDX=$(python $CHIPYARD_ROOT/vlsi/autoflow/gen_boom_config.py)
    echo "BOOM configuration index = $BOOM_CFG_IDX"
    BOOM_CFG_NAME="Boom${BOOM_CFG_IDX}Config"

    make buildfile CONFIG=$BOOM_CFG_NAME
    make redo-syn CONFIG=$BOOM_CFG_NAME

done
