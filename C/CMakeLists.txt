cmake_minimum_required(VERSION 2.8)
project(Beamforming)

include_directories(${CMAKE_SRC_DIR}/include)

set(SRC main.cpp)
add_executable(Beamforming ${SRC})

find_package(GSL REQUIRED)    
find_package(HDF5 REQUIRED)
include_directories(${HDF5_INCLUDE_DIR})

target_link_libraries(Beamforming GSL::gsl GSL::gslcblas hdf5 hdf5_cpp)
