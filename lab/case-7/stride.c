#include <assert.h>
#include "dataset.h"
#include "hpm.h"


void __attribute__ ((noinline)) stride(vec_t vec)
{
    size_t i, j;
    
    // for each vector, access every block with cache line size
    for (i = 0; i < LEN_VEC; i += INT_PER_CACHE_LINE * STRIDE) {

        // for current cache line, do some operations
        for (j = 0; j < NUM_OP; j++) {
            vec[i + j % 4] += 1;
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
