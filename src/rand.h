#pragma once

#include <cstdlib>

#ifdef __APPLE__
struct drand48_data {
    unsigned short xsubi[3];
};

inline int drand48_r(drand48_data *buffer, double *result) {
    *result = erand48(buffer->xsubi);
    return 0;
}
#endif


class ThreadSafeRandom
{
public:
    static double nextDouble()
    {
        double res = 0.0;
        drand48_r(&rand_state, &res);
        return res;
    }

private:
    static __thread drand48_data rand_state;
};
