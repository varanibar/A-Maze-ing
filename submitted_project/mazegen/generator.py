# Built-in modules
import sys
import random

# Project modules
from .maze import Maze
from .solver import MazeSolver


class MazeGenerator:
    """
    Generate and store a maze from validated configuration parameters.

    Handles input validation, random seed initialization, entry and exit
    positions, reserved cells, and the data structures used during maze
    generation.
    """
    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
        maze_entry: tuple[int, int] = (0, 0),
        maze_exit: tuple[int, int] | None = None,
        seed: int | None = None,
        perfect: bool = True
    ) -> None:
        """
        Initialize a maze generator with the given configuration.

        Validates the input parameters, initializes the random seed,
        creates the maze, and prepares the structures used for maze
        generation.
        """
        try:
            self._parse_input(
                width,
                height,
                maze_entry,
                maze_exit,
                seed,
                perfect
                )

        except Exception as err:
            print(f"Parsing error ({err.__class__.__name__}): {err}")
            return

        if seed is not None:
            random.seed(seed)
            self.seed = seed
            self.random_seed = -1
        elif seed is None:
            random_seed = random.randint(0, 10000000000000000)
            random.seed(random_seed)
            self.seed = -1
            self.random_seed = random_seed

        self.maze = Maze(self.width, self.height)

        self.reserved_cells = self._get_42_cells()

        self.visited: set[tuple[int, int]] = {self.entry}
        self.stack: list[tuple[int, int]] = [self.entry]

        self.ways = {
            "N": (0, -1, 1, 4),
            "E": (1, 0, 2, 8),
            "S": (0, 1, 4, 1),
            "W": (-1, 0, 8, 2),
        }

        for x, y in self.reserved_cells:
            self.visited.add((x, y))

    def _parse_input(
                    self,
                    raw_width: int | None,
                    raw_height: int | None,
                    raw_entry: tuple[int, int],
                    raw_exit: tuple[int, int] | None,
                    raw_seed: int | None,
                    raw_perfect: bool = True
                    ) -> None:
        """
        Validate and store the maze generation parameters.

        Checks the maze dimensions, entry and exit coordinates, seed, and
        perfect-maze option. Converts validated values when needed and stores
        them as instance attributes.

        Raises:
            TypeError: If WIDTH or HEIGHT is missing.
            ValueError: If any argument has an invalid type, value, format,
                or coordinate outside the maze bounds.
        """

        # WIDTH / HEIGHT
        if raw_width is None or raw_height is None:
            raise TypeError(
                "Missing required positional arguments: 'width', 'height'"
                )

        if not isinstance(raw_width, int) or not isinstance(raw_height, int):
            raise ValueError(
                "WIDTH and HEIGHT must be of type integer."
                )

        try:
            width = int(raw_width)
            height = int(raw_height)
        except (TypeError, ValueError):
            raise ValueError(
                "WIDTH and HEIGHT must be valid integers."
                )

        if width <= 1 or height <= 1:
            raise ValueError(
                "WIDTH and HEIGHT must be greater than 1."
                )

        self.width = width
        self.height = height

        # ENTRY
        if not isinstance(raw_entry, tuple) or len(raw_entry) != 2:
            raise ValueError(
                "ENTRY must be formated as (x, y)"
                )

        try:
            x_entry = int(raw_entry[0])
            y_entry = int(raw_entry[1])
        except (TypeError, ValueError):
            raise ValueError(
                "ENTRY must be valid integers in format: (x, y)"
                )

        # EXIT
        if raw_exit is None:
            x_exit = width - 1
            y_exit = height - 1
        else:
            if not isinstance(raw_exit, tuple) or len(raw_exit) != 2:
                raise ValueError(
                    "EXIT must be formated as (x, y)"
                    )

            try:
                x_exit = int(raw_exit[0])
                y_exit = int(raw_exit[1])
            except (TypeError, ValueError):
                raise ValueError(
                    "EXIT must be valid integers in format: (x, y)"
                    )

        # COORDINATES VALIDATION
        if x_entry < 0 or y_entry < 0:
            raise ValueError(
                "ENTRY coordinates must be positive integers."
                )
        if x_exit < 0 or y_exit < 0:
            raise ValueError(
                "EXIT coordinates must be positive integers."
                )

        if not (
            0 <= x_entry < self.width
            and 0 <= y_entry < self.height
        ):
            raise ValueError(
                "ENTRY coordinates is out of grid bounds."
                )

        if not (
            0 <= x_exit < self.width
            and 0 <= y_exit < self.height
        ):
            raise ValueError(
                "EXIT coordinates is out of grid bounds."
                )

        self.entry = (x_entry, y_entry)
        self.exit = (x_exit, y_exit)

        if self.entry == self.exit:
            raise ValueError(
                "ENTRY and EXIT coordinates cannot be identical"
                )

        if raw_seed is not None:
            try:
                seed = int(raw_seed)
            except ValueError:
                raise ValueError(
                    "SEED must be a valid integer"
                    )
            if seed < 0:
                raise ValueError(
                    "SEED must be a positive integer"
                    )

            self.seed = seed

        # PERFECT
        if isinstance(raw_perfect, bool):
            self.perfect = raw_perfect

        else:
            raise ValueError(
                "PERFECT must be True or False."
            )

    def _get_42_cells(self) -> set[tuple[int, int]]:
        """Returns the set of (x, y) coordinates forming the '42' logo.
        Omits the logo and logs to stderr if the grid is too small or if
        the entry/exit points collide with the pattern.
        """
        if self.maze.width < 9 or self.maze.height < 7:
            print(
                "Warning: Maze size is too small for '42' pattern. "
                "Omitting pattern.",
                file=sys.stderr,
            )
            return set()

        cx = self.maze.width // 2
        cy = self.maze.height // 2

        # Offsets relative to center (dx, dy)
        offsets = [
            # Digit '4'
            (-3, -2),
            (-3, -1),
            (-3, 0),
            (-2, 0),
            (-1, 0),
            (-1, 1),
            (-1, 2),
            # Digit '2'
            (1, -2),
            (2, -2),
            (3, -2),
            (3, -1),
            (1, 0),
            (2, 0),
            (3, 0),
            (1, 1),
            (1, 2),
            (2, 2),
            (3, 2),
        ]

        reserved = set()
        for dx, dy in offsets:
            cell_x = cx + dx
            cell_y = cy + dy

            if (
                0 <= cell_x < self.maze.width
                and 0 <= cell_y < self.maze.height
            ):
                reserved.add((cell_x, cell_y))

        if self.entry in reserved or self.exit in reserved:
            print(
                "Warning: Entry or exit point collides with '42' pattern. "
                "Omitting pattern.",
                file=sys.stderr,
            )
            return set()

        return reserved

    def generate(self) -> None:
        """Run DFS generation and apply imperfection if configured."""

        while self.stack:
            curr_x, curr_y = self.stack[-1]
            neighbors = []

            for name, (dir_x, dir_y, curr_bit, n_bit) in self.ways.items():
                neighbor_x, neighbor_y = curr_x + dir_x, curr_y + dir_y

                if (
                    0 <= neighbor_x < self.maze.width
                    and 0 <= neighbor_y < self.maze.height
                ):
                    if (neighbor_x, neighbor_y) not in self.visited:
                        neighbors.append(
                            (neighbor_x, neighbor_y, curr_bit, n_bit)
                        )

            if neighbors:
                neighbor_x, neighbor_y, curr_bit, n_bit = random.choice(
                    neighbors
                )

                # Carve a two-way passage by removing walls from
                # both adjacent cells:
                # 1. '~curr_bit' creates a bitmask where all bits
                # are 1 except the targeted wall bit (0).
                # 2. '&=' applies bitwise AND to clear (set to 0)
                # that specific wall bit on the current cell.
                self.maze.cells[(curr_x, curr_y)] &= ~curr_bit
                # 3. Repeat for the neighbor cell using 'n_bit'
                # to open the matching opposite wall.
                self.maze.cells[(neighbor_x, neighbor_y)] &= ~n_bit

                self.visited.add((neighbor_x, neighbor_y))
                self.stack.append((neighbor_x, neighbor_y))

            else:
                self.stack.pop()

        if not self.perfect:
            self.make_imperfect()

        self.solver = MazeSolver(
            self.maze.cells,
            self.entry,
            self.exit,
            self.maze.height,
            self.maze.width
            )

    def get_solution(self) -> str:
        """Return solution path string using internal solver."""
        return "".join(self.solver.path.values())

    def render(self, show_solution: bool = False) -> str:
        """Delegate visual rendering to internal maze grid."""
        path_cells = None
        if show_solution:
            path_cells = set(self.solver.path.keys())
            path_cells.add(self.exit)

        return self.maze.render(
            path_cells=path_cells,
            entry=self.entry,
            exit=self.exit,
        )

    def to_hex_grid(self) -> str:
        """Delegate hex grid generation to internal maze grid."""
        return self.maze.to_hex_grid()

    def make_imperfect(self) -> None:
        """Convert a perfect maze into an imperfect maze
        with multiple paths.

        Introduces cycles and alternative routes by opening
        walls at key landmark
        cells, creating random loops throughout the grid,
        and removing dead ends.
        """
        self._open_key_locations()
        self._create_loops()
        self._remove_dead_ends()

    def _open_key_locations(self) -> None:
        """Open a random wall at strategic key locations
        across the grid.

        Targets five focal points, the four grid corners and
        the center cell, and carves open an adjacent wall
        for each to increase spatial connectivity.
        """
        center_x = self.maze.width // 2
        center_y = self.maze.height // 2

        key_cells = [
            (0, 0),  # top-left
            (self.maze.width - 1, 0),  # top-right
            (0, self.maze.height - 1),  # bottom-left
            (self.maze.width - 1, self.maze.height - 1),  # bottom-right
            (center_x, center_y),  # center
        ]

        for x, y in key_cells:
            self._open_random_wall(x, y)

    def _create_loops(self) -> None:
        """Randomly knocks down interior walls to create loops."""
        for x in range(self.maze.width - 1):
            for y in range(self.maze.height - 1):
                if random.random() < 0.15:
                    self._open_random_wall(x, y)

    def _remove_dead_ends(self) -> None:
        """Repeatedly finds cells with 3 walls intact and opens one side
        until none remain.
        """
        has_dead_ends = True

        while has_dead_ends:
            has_dead_ends = False
            for x in range(self.maze.width):
                for y in range(self.maze.height):
                    if (x, y) in self.reserved_cells:
                        continue
                    if self._count_walls(x, y) == 3:
                        if self._open_random_wall(x, y):
                            has_dead_ends = True

    def _count_walls(self, x: int, y: int) -> int:
        """Counts how many of the 4 walls are closed for a cell."""
        cell_value = self.maze.cells[(x, y)]
        walls = 0

        if cell_value & 1:
            walls += 1
        if cell_value & 2:
            walls += 1
        if cell_value & 4:
            walls += 1
        if cell_value & 8:
            walls += 1

        return walls

    def _is_3x3_fully_open(self, bx: int, by: int) -> bool:
        """Checks if a 3x3 block starting at top-left corner (bx, by)
        has no internal walls.
        """
        east_wall = 2
        south_wall = 4

        for col in range(3):
            for row in range(3):
                cell_walls = self.maze.cells[(bx + col, by + row)]

                # Check East wall for the first 2 columns
                if col < 2 and (cell_walls & east_wall):
                    return False

                # Check South wall for the first 2 rows
                if row < 2 and (cell_walls & south_wall):
                    return False

        return True  # All internal walls are gone

    def _creates_3x3_open_area(
        self, x: int, y: int, nx: int, ny: int
    ) -> bool:
        """Determine if removing the wall between two cells
        creates an open 3x3 space.

        Evaluates all overlapping 3x3 sub-grids that contain
        the wall between cell (x, y) and neighbor cell (nx, ny).

        How it works:
        1. Identify Overlapping Origins: A single wall segment
        can belong to up to six overlapping 3x3 blocks.
           - Horizontal wall removal (nx != x) checks 2
           column origins by 3 row origins.
           - Vertical wall removal (ny != y) checks 3
           column origins by 2 row origins.
        2. Boundary Validation: Filters out candidate 3x3 blocks
         whose outer coordinates (bx + 2, by + 2) fall outside
         the maze boundaries.
        3. Open Area Check: Delegates each valid candidate
         block to `_is_3x3_fully_open` to inspect whether all internal
         walls within that 3x3 area are carved out.

        Args:
            x (int): X-coordinate of the primary cell.
            y (int): Y-coordinate of the primary cell.
            nx (int): X-coordinate of the adjacent target cell.
            ny (int): Y-coordinate of the adjacent target cell.

        Returns:
            bool: True if opening the wall produces at
            least one completely open 3x3 block of cells; False otherwise.
        """
        # Find overlapping 3x3 block origins (bx, by) based on wall direction
        col_range: tuple[int, ...]
        row_range: tuple[int, ...]
        if nx != x:  # Horizontal movement
            col_range = (x - 1, x)
            row_range = (y - 2, y - 1, y)
        else:  # Vertical movement
            col_range = (x - 2, x - 1, x)
            row_range = (y - 1, y)

        for bx in col_range:
            for by in row_range:
                # Skip blocks that spill outside maze boundaries
                if (
                    0 <= bx
                    and (bx + 2) < self.maze.width
                    and 0 <= by
                    and (by + 2) < self.maze.height
                ):
                    if self._is_3x3_fully_open(bx, by):
                        return True

        return False

    def _open_random_wall(self, x: int, y: int) -> bool:
        """Attempts to break a CLOSED wall between (x, y) and a neighbor
        without creating a 3x3 room.
        """
        if (x, y) in self.reserved_cells:
            return False

        directions = list(self.ways.keys())
        random.shuffle(directions)

        for direction in directions:
            dx, dy, curr_bit, n_bit = self.ways[direction]
            nx, ny = x + dx, y + dy

            # Skip invalid neighbors or walls that are already open
            if not (0 <= nx < self.maze.width and 0 <= ny < self.maze.height):
                continue
            if (nx, ny) in self.reserved_cells:
                continue

            is_wall_closed = bool(self.maze.cells[(x, y)] & curr_bit)
            if not is_wall_closed:
                continue

            # Tentatively open the wall
            self.maze.cells[(x, y)] &= ~curr_bit
            self.maze.cells[(nx, ny)] &= ~n_bit

            # Check rule violation & rollback if necessary
            if self._creates_3x3_open_area(x, y, nx, ny):
                self.maze.cells[(x, y)] |= curr_bit  # Restore wall
                self.maze.cells[(nx, ny)] |= n_bit  # Restore wall
                continue

            # Success! Wall stays open
            return True

        return False
