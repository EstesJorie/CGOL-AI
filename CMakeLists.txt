cmake_minimum_required(VERSION 3.14)
project(GameOfLife LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

if(NOT DEFINED PYTHON_EXECUTABLE)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
else()
    message(STATUS "Using manually specified Python executable: ${PYTHON_EXECUTABLE}")
    find_package(Python COMPONENTS Interpreter Development REQUIRED
                 PATHS ${PYTHON_EXECUTABLE} NO_DEFAULT_PATH)
endif()

add_subdirectory(pybind11)

include_directories(${pybind11_INCLUDE_DIRS})

message(STATUS "Using Python executable: ${Python_EXECUTABLE}")
message(STATUS "Using Python include dirs: ${Python_INCLUDE_DIRS}")

pybind11_add_module(GameOfLife CGOL_Bindings.cpp cgol.cpp)

target_link_libraries(GameOfLife PRIVATE Python::Python)
