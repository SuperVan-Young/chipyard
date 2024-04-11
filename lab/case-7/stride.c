#include <assert.h>
#include "dataset.h"
#include "hpm.h"


void __attribute__ ((noinline)) stride(vec_t vec)
{
    size_t i;
    
    // for each vector, access every block with cache line size
    for (i = 0; i < LEN_VEC; i += INT_PER_CACHE_LINE * STRIDE) {

        vec[i+1] = vec[i];

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
