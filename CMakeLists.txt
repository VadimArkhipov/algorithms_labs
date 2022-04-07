cmake_minimum_required(VERSION 3.21)
project(untitled)

set(CMAKE_CXX_STANDARD 17)

add_executable(untitled main.cpp prefix_func.h prefix_func.cpp KMP.h KMP.cpp is_cycle.h is_cycle.cpp)
