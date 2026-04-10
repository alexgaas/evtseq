cmake_minimum_required(VERSION 4.0)
project(evtseq)

set(CMAKE_CXX_STANDARD 17)

add_executable(evtseq main.cpp
        src/rand.cpp
        src/rand.h
        src/prob_counter.h
        src/activity_counter.h
        src/interval_set.h
)

add_library(prob_counter_shared SHARED
        src/prob_counter_wrapper.cpp
        src/rand.cpp
)

set_target_properties(prob_counter_shared PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)

add_library(interval_set_shared SHARED
        src/interval_set_wrapper.cpp
)

set_target_properties(interval_set_shared PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)

add_library(activity_counter_shared SHARED
        src/activity_counter_wrapper.cpp
)

set_target_properties(activity_counter_shared PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)
