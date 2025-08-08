## Project Structure

CGOL/
├── CMakeLists.txt
├── cgol.cpp            #CGOL C++ Source
├── cgol.hpp              #CGOL Header File
├── CGOL_Bindings.cpp         #pybind11 bindings for Python
├── README.md

---

## Prerequisites

- C++ compiler supporting C++14 or later (GCC, Clang, MSVC)
- Python 3.x development headers
- CMake (3.14+ recommended)
- pybind11 Python package

---

## Build

1. **Install pybind11 Python package**
```bash
pip install pybind11
```

2. **Build C++ Source**
```bash
cd build
cmake ..
cmake --build .
```
3. **Running the API (api.py)**

If not previously installed:
```bash
pip install fastapi uvicorn pydantic
```

Run the API server:
```bash
unvicorn api.py:app --reload
```

(Optional) - Test the API:
```bash
curl -X POST "http://127.0.0.1:8000/cgol" -H "Content-Type: application/json" -d '{"word": "monument"}'
```

This should return:
```json
{
  "generations": 4,
  "score": 38
}
```

4. Python Client Conway CLI (cgoltool.py)
To run the script, in the terminal:
```bash
python cgtool.py
```

You will be prompted for four pieces of information:
1. API URL, generated from Step 3
2. GPT-4o API URL
3. GPT-4o API KEY
4. Content-Type header

Once provided, you can enter prompts like:
> How many generations will the word 'monument' return from the Conway tool?
> Generate 3 random words and tell me the highest Conway score.

Once complete, you can then type exit to quit.
```bash
exit
```
