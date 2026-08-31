class MazeSolver:
    """
    Solve a maze using breadth-first search.

    Explores reachable cells from the entry, records how each cell was
    reached, then reconstructs the path from the exit back to the entry.
    """
    def __init__(
                self,
                cells: dict[tuple[int, int], int],
                entry: tuple[int, int],
                exit: tuple[int, int],
                height: int,
                width: int
                ) -> None:
        """
        Initialize the solver and compute the path through the maze.
        """
        self.cells = cells
        self.entry = entry
        self.exit = exit
        self.height = height
        self.width = width
        self.visited: set[tuple[int, int]] = {self.entry}
        self.stack: list[tuple[int, int]] = []
        self.path: dict[tuple[int, int], str] = {}
        self.queue: list[tuple[int, int]] = [self.entry]
        self.came_from: dict[
                            tuple[int, int],
                            tuple[tuple[int, int], str]
                            ] = {}

        while self.queue:
            current_cell = self.queue.pop(0)
            available_neighbors = self._get_neighbors(current_cell)
            if available_neighbors:
                for (neighbor, direction) in available_neighbors.items():
                    self.came_from[neighbor] = (current_cell, direction)
                    self.visited.add(neighbor)
                    self.queue.append(neighbor)

        current_cell = self.exit
        self.stack = [current_cell]

        while current_cell != self.entry:
            current_cell = self.came_from[current_cell][0]
            self.stack.append(current_cell)

        self.stack.reverse()

        for current_cell in self.stack[1:]:
            previous_cell = self.came_from[current_cell][0]
            direction = self.came_from[current_cell][1]
            self.path[previous_cell] = direction

    def _is_not_visited(self, neighbor: tuple[int, int]) -> bool:
        """Return whether the neighboring cell has not been visited."""
        if neighbor in self.visited:
            return False
        return True

    def _is_wall_open(self, bit: int) -> bool:
        """Return whether the wall represented by the given bit is open."""
        if bit:
            return False
        return True

    def _is_in_bounds(self, neighbor: tuple[int, int]) -> bool:
        """Return whether the neighboring cell is inside the maze bounds."""
        x = neighbor[0]
        y = neighbor[1]
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def _is_available(self, wall: int, neighbor: tuple[int, int]) -> bool:
        """
        Return whether a neighboring cell can be visited.

        A cell is available if it is inside the maze, the connecting wall
        is open, and the cell has not already been visited.
        """
        if (
            self._is_in_bounds(neighbor)
            and self._is_wall_open(wall)
            and self._is_not_visited(neighbor)
                ):
            return True
        return False

    def _get_neighbors(
            self,
            current_cell: tuple[int, int]
            ) -> dict[tuple[int, int], str]:
        """
        Find all available neighboring cells.

        Returns:
            A dictionary mapping each available neighboring cell to the
            direction used to reach it.
        """
        key = current_cell
        value = self.cells[key]
        x = current_cell[0]
        y = current_cell[1]
        available_neighbors = {}

        west = ("W", value >> 3, -1, 0)
        south = ("S", (value >> 2) % 2, 0, 1)
        east = ("E", (value >> 1) % 2, 1, 0)
        north = ("N", value % 2, 0, -1)
        directions = [west, south, east, north]

        for (name, wall, dx, dy) in directions:
            neighbor: tuple[int, int] = (x + dx, y + dy)
            direction = name
            if self._is_available(wall, neighbor):
                available_neighbors[neighbor] = direction
        return available_neighbors
