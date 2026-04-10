#include "rand.h"
#include "prob_counter.h"

__thread drand48_data ThreadSafeRandom::rand_state;

PrecalcedCounter ProbabilisticCounter::precalced;

ThreadSafeRandom ProbabilisticCounter::random;