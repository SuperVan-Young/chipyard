/* 
    Sequentially traverse the vector with two strides
 */

#ifndef DATASET_H
#define DATASET_H

#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>

// cache line is 64 Bytes, int is 4 Bytes
#define INT_PER_CACHE_LINE 16

// length of the vector
#define LEN_VEC 5 * 1024

// how many cache line in every iteration
#define STRIDE_1 2

#define STRIDE_2 3

// number of incr operations on every cache line
#define NUM_OP 16

typedef intptr_t vec_t[LEN_VEC];

/* Force test_vec to be allocated in .data */
static vec_t test_vec = { 1 };

#endif  /* DATASET_H */