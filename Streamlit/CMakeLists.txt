cmake_minimum_required(VERSION 3.15)
project(correlation)

set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 REQUIRED)

pybind11_add_module(correlation utils/correlation.cpp)


install(TARGETS correlation LIBRARY DESTINATION .)