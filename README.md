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
```

- WIDTH: Maze width (number of cells)
- HEIGHT: Maze height
- ENTRY: Entry coordinates (x,y)
- EXIT: Exit coordinates (x,y)
- OUTPUT_FILE: Output filename
- PERFECT: Is the maze perfect?

# Maze Generation Algorithm
- Chosen Algorithm: Recursive Backtracking (Depth-First Search).

- Why: It is straightforward to implement, guarantees a single valid path between any two points (perfect maze), and produces long, winding corridors that are visually engaging to solve.

# Reusable Package (***mazegen***)
The core generation logic is isolated inside the mazegen package as a standalone ***MazeGenerator*** class.

## Usage Documentation

### 1. Instantiate and Generate a Basic Maze
```python
from mazegen import Maze, MazeGenerator

# Initialize the grid with width and height
grid = Maze(width=21, height=11)

# Pass entry and exit points to the generator
builder = MazeGenerator(grid, maze_entry=(0, 0), maze_exit=(20, 10))

# Run the generation algorithm
builder.generate()

```

### 2. Custom Parameters (Seed & Imperfect Mazes)
```Python
import random

# Set a seed for reproducible generation
random.seed(42)

# Optional: add loops/multiple paths to make the maze non-perfect
builder.make_imperfect()

```

### 3. Access Structure & Solution

```python
# Render the maze string
maze_string = grid.render()

# Access the raw hex grid structure
hex_grid = grid.to_hex_grid()

# Access the solution path from entry to exit
solution_path = builder.get_solution()

```

# Team and Project Management

**Team Roles:**

pride-ol: Generation algorithm and package structure (mazegen), Configuration parsing

varaniba: rendering/display, solver algorithm.

**Planning:** We broke the project into milestones (Algorithm -> Packaging -> Display -> Error Handling). The timeline held up well, though visualization edge cases took longer than expected.

**What Worked Well:** Strict separation of the generator package from the main UI script made debugging and writing unit tests much easier.

**Improvements:** Earlier integration testing between the config parser and the grid constraints would have caught terminal-size mismatch errors faster.

**Tools Used:** Git, Python (venv, build, mypy, flake8), Makefile.

Resources & AI Usage
Resources
....

# AI Usage

Helped troubleshooting Makefile subshell behaviors and virtual environment paths.

Helped understand how to structure the pyproject.toml, create documentations.

