#include <assert.h>
#include "dataset.h"
#include "hpm.h"


void __attribute__ ((noinline)) stride(vec_t vec)
{
    size_t i, j, k;
    size_t arr_beg[NUM_VEC] = {0};   // starting point in this turn
    size_t arr_idx[NUM_VEC] = {0};   // current index in the vector
    
    // for each vector, access every block with cache line size
    for (i = 0; i < LEN_VEC; i += INT_PER_CACHE_LINE) {

        // access one cache line in each iteration
        for (j = 0; j < NUM_VEC; j++) {

            size_t idx = arr_idx[j];

            // operate on the cache line for a while
            int num_op = arr_num_op[j];
            for (k = 0; k < num_op; k++) {
                vec[j][idx+k] = vec[j][idx+k] + 1;
            }

            // update idx
            idx += arr_stride[j] * INT_PER_CACHE_LINE;
            if (idx >= LEN_VEC) {
                arr_beg[j] += INT_PER_CACHE_LINE;
                arr_idx[j] = arr_beg[j];
            } else {
                arr_idx[j] = idx;
            }
        }
    }
}

int main(void)
{
    /* Enable performance counters */
    hpm_init();

    stride(test_vec);

    /* Print performance counter data */
    hpm_print();

    return 0;
}
