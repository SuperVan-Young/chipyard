#include <assert.h>
#include "hpm.h"

#define N 4096
#define STRIDE 4
#define INT_PER_CACHELINE 16

typedef intptr_t vec_t[N];

static vec_t src = {0};

void __attribute__ ((noinline)) stride(vec_t a)
{
    size_t i, j, k;
    
    for (k = 0; k < STRIDE; k++) {
        /* Iterate through sub-sequence */

        size_t start = k * INT_PER_CACHELINE;
        size_t j_stride = STRIDE * INT_PER_CACHELINE;

        for (j = start; j < N; j += j_stride) {

            /* Increase within a cache line, unroll by 4 */
            for (i = 0; i < 4; i++) {
                a[j+i*4] = 1;
                a[j+i*4+1] = 1;
                a[j+i*4+2] = 1;
                a[j+i*4+3] = 1;
            }
        }
    }
}

int main(void)
{
    /* Enable performance counters */
    hpm_init();

    stride(src);

    /* Print performance counter data */
    hpm_print();

    return 0;
}
