#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "cgol.hpp"

namespace py = pybind11;

PYBIND11_MODULE(GameOfLife, m) {
    m.doc() = "Game of Life bindings";
    
    m.def("game_of_life", &gameOfLife, "Run Game of Life with word seed",
          py::arg("word"));
}
