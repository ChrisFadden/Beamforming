cmake_minimum_required(VERSION 2.8)
project(Beamforming)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -Wpedantic -fcolor-diagnostics")

#****************
#Enable OpenMP 
#****************
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp")

#************************
#	Set Include/Module dirs
#************************
include_directories(./include)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")

#***************
#	Add src files
#***************
set(SRC main.cpp)
add_executable(Beamforming ${SRC})

#**************************
#	Link to external packages
#**************************
find_package(HDF5 REQUIRED)
include_directories(${HDF5_INCLUDE_DIR})

find_package(MPI REQUIRED)
include_directories(${MPI_INCLUDE_PATH})

find_package(Armadillo REQUIRED)
include_directories(${ARMADILLO_INCLUDE_DIR})

find_package(BLAS REQUIRED)
include_directories(${BLAS_INCLUDE_DIR})

target_link_libraries(Beamforming hdf5 ${MPI_LIBRARIES} 
	${ARMADILLO_LIBRARIES} ${BLAS_LIBRARIES} ${CMAKE_SOURCE_DIR}/libs/pogs.a)

set_target_properties(Beamforming PROPERTIES COMPILE_FLAGS "${MPI_COMPILE_FLAGS}")
set_target_properties(Beamforming PROPERTIES LINK_FLAGS "${MPI_LINK_FLAGS}")

