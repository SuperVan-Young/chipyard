/* 
    Sequentially traverse the vector with a stride of 4 cache block.
    This time even more memory intensive!
 */

#ifndef DATASET_H
#define DATASET_H

#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>

// cache line is 64 Bytes, int is 4 Bytes
#define INT_PER_CACHE_LINE 16

// length of the vector
#define LEN_VEC 4096

// how many cache line in every iteration
#define STRIDE 4

typedef intptr_t vec_t[LEN_VEC];

/* Force test_vec to be allocated in .data */
static vec_t test_vec = { 1 };

#endif  /* DATASET_H */