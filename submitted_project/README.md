*This project has been created as part of the 42 curriculum by pride-ol, varaniba.*

# Description
A-Maze-Ing is a Python application designed to generate, solve, and display mazes. The main goal of this project is to implement algorithmic generation, clean terminal or graphical visualization, and package the core logic into a reusable library (mazegen) for future projects.

# Instructions

**Installation**

```
python3 -m venv .venv
source .venv/bin/activate
pip install flake8 mypy build
```

**Execution**

Run the main program using a configuration file:

```
python3 a_maze_ing.py config.txt
```

**Building the Package**

To build the mazegen package distribution artifacts:

```
pip install build
python3 -m build
cp dist/* .
```

# Config File Structure
The ***config.txt*** file controls the maze parameters.

Example format:

```
Plaintext
WIDTH=9
HEIGHT=7
ENTRY=0,0
EXIT=8,6
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42
```

- WIDTH: Maze width (number of cells)
- HEIGHT: Maze height
- ENTRY: Entry coordinates (x,y)
- EXIT: Exit coordinates (x,y)
- OUTPUT_FILE: Output filename
- PERFECT: Is the maze perfect?
- SEED(OPTIONAL): A random positive integer.

# Maze Generation Algorithm
- Chosen Algorithm: Recursive Backtracking (Depth-First Search).

- Why: It is straightforward to implement, guarantees a single valid path between any two points (perfect maze), and produces long, winding corridors that are visually engaging to solve.

# Maze Solving Algorithm
- Chosen Algorithm: Recursive Backtracking (Breadth-First Search).

- Why: Just as the maze generation algorithm, it is straightforward to implement. It explores reachable cells from the entry, records how each cell was reached, then reconstructs the path from the exit back to the entry.

# Reusable Package (***mazegen***)
The core generation logic is isolated inside the mazegen package as a standalone ***MazeGenerator*** class.

## Usage Documentation

### 1. Install package

```
python3 install mazegen-0.1.0-py3-none-any.whl

```

### 2. Instantiate and Generate a Basic Maze
```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=12, height=12)
gen.generate()

# Print the ASCII string to your terminal
print(gen.render())

```

### 3. Custom Parameters (Seed & Imperfect Mazes)
```Python
from mazegen import MazeGenerator

# Create a reproducible, imperfect maze (contains loops and multiple paths)
gen = MazeGenerator(
    width=15,
    height=15,
    seed=42,         # Set seed for reproducible generation
    perfect=False    # Set to False to allow extra open paths/loops
)
gen.generate()

```

### 4. Access Structure & Solution

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=12, height=12)
gen.generate()

# Print maze with entry, exit, and path overlay
print(gen.render(show_solution=True))

# Access the solution path string from entry to exit (e.g., "SSEEWW...")
solution_path = gen.get_solution()

```

# Team and Project Management

**Team Roles:**

pride-ol: Generation algorithm (DFS) and package structure (mazegen), configuration file parsing

varaniba: rendering/display using the Curses Python module, solver algorithm (BFS), reusable package parsing.

**Planning:** We broke the project into milestones (Algorithm -> Packaging -> Display -> Error Handling). The timeline held up well, though visualization edge cases took longer than expected.

**What Worked Well:** Strict separation of the generator package from the main UI script made debugging and writing unit tests much easier.

**Improvements:** Earlier integration testing between the config parser and the grid constraints would have caught terminal-size mismatch errors faster. Some of the code structure related to the UI can be optimized.

**Tools Used:** Git, Python (venv, build, mypy, flake8), Makefile.

# Resources
The references and tools used were:
- W3 schools [website](https://www.w3schools.com/)
- GeeksforGeeks [website](https://www.geeksforgeeks.org/)
- Stack Overflow [website](https://stackoverflow.com/questions)
- Github [website](https://github.com/)
- Peers from the Codam March 2026 cohort.

# AI Usage

Helped troubleshooting Makefile behaviors and virtual environment paths.

Helped understand how to structure the pyproject.toml and create documentations.

Clarified new complex concepts from Curses and Packages.

