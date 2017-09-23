cmake_minimum_required(VERSION 2.8)
project(Beamforming)

include_directories(${CMAKE_SRC_DIR}/include)
include_directories(/usr/include/ecos/)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")

set(SRC main.c)
add_executable(Beamforming ${SRC})

find_package(HDF5 REQUIRED)
include_directories(${HDF5_INCLUDE_DIR})

find_package(MPI REQUIRED)
include_directories(${MPI_INCLUDE_PATH})

find_package(CBLAS REQUIRED)
find_package(LAPACK REQUIRED)

target_link_libraries(Beamforming hdf5 ${MPI_LIBRARIES} ${CBLAS_LIBRARIES} ${LAPACK_LIBRARIES})

set_target_properties(Beamforming PROPERTIES COMPILE_FLAGS "${MPI_COMPILE_FLAGS}")
set_target_properties(Beamforming PROPERTIES LINK_FLAGS "${MPI_LINK_FLAGS}")

