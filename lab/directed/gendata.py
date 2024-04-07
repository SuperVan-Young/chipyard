#!/usr/bin/env python3
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('rows', type=int, default=256, nargs='?')
parser.add_argument('cols', type=int, default=64, nargs='?')
args = parser.parse_args()

print(''' /* Generated by {} */
#ifndef DATASET_H
#define DATASET_H

#include <stdint.h>

#define MAT_M {}
#define MAT_N {}

typedef intptr_t mat_mxn_t[MAT_M][MAT_N];
typedef intptr_t mat_nxm_t[MAT_N][MAT_M];

/* Force test_dst to be allocated in .data */
static mat_nxm_t test_dst = {{ {{ 1 }} }};
const static mat_mxn_t test_src = {{'''.format(__file__, args.rows, args.cols));

for i in range(args.rows):
    print('\t{ ', end='')
    for j in range(args.cols):
        print('{},'.format(int(random.uniform(-0x80000000, 0x80000000))), end='')
    print(' },')

print('''};

#endif /* DATASET_H */''');
