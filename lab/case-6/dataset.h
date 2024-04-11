/* 
    Sequentially traverse the vector with a stride of 1 cache block.
    This time it's more memory intensive!
 */

#ifndef DATASET_H
#define DATASET_H

#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>

// cache line is 64 Bytes, int is 4 Bytes
#define INT_PER_CACHE_LINE 16

// length of the vector
#define LEN_VEC 1024

// how many cache line in every iteration
#define STRIDE 1

// number of incr operations on every cache line
#define NUM_OP 4

typedef int vec_t[LEN_VEC];

/* Force test_vec to be allocated in .data */
static vec_t test_vec = { 1 };

#endif  /* DATASET_H */