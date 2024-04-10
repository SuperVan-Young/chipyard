/* 
    Traverse 4 vectors with diversified strides.
 */

#ifndef DATASET_H
#define DATASET_H

#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>

// cache line is 64 Bytes, int is 4 Bytes
#define INT_PER_CACHE_LINE 16

// number of vectors
#define NUM_VEC 4

// length of every vector
#define LEN_VEC 1024

typedef intptr_t vec_t[NUM_VEC][LEN_VEC];

/* Force test_vec to be allocated in .data */
static vec_t test_vec = { { 1 } };

// how many cache line in every iteration
static size_t arr_stride[NUM_VEC] = {1, 3, 5, 7};

// number of incr operations on every cache line
// This can vary between 1 ~ 16
static size_t arr_num_op[NUM_VEC] = {16, 16, 16, 16};

#endif  /* DATASET_H */