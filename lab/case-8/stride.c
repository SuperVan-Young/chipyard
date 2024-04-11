#include <assert.h>
#include "dataset.h"
#include "hpm.h"


void __attribute__ ((noinline)) stride(vec_t vec_1, vec_t vec_2)
{
    size_t i, j;
    size_t beg = 0;   // starting point of this vector traversal
    size_t idx = 0;   // starting point of this block
    
    // for each vector, access every block with cache line size
    for (i = 0; i < LEN_VEC; i += INT_PER_CACHE_LINE) {

        // for current cache line, do some operations
        for (j = 0; j < NUM_OP; j++) {
            vec_2[idx + j % INT_PER_CACHE_LINE] += vec_1[idx + j % INT_PER_CACHE_LINE];
        }

        // update idx 
        idx += INT_PER_CACHE_LINE * STRIDE;
        if (idx >= LEN_VEC) {
            beg += INT_PER_CACHE_LINE;
            idx = beg;
        }

    }
}

int main(void)
{
    /* Enable performance counters */
    hpm_init();

    stride(src_vec, test_vec);

    /* Print performance counter data */
    hpm_print();

    return 0;
}
