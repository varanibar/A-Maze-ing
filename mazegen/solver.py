# Project modules
from mazegen.generator import MazeGenerator


class MazeSolver:
    def __init__(
                self,
                builder: MazeGenerator
                ) -> None:

        self.cells = builder.maze.cells
        self.entry = builder.entry
        self.exit = builder.exit
        self.height = builder.maze.height
        self.width = builder.maze.width
        self.visited: set[tuple[int, int]] = {self.entry}
        self.stack: list[tuple[int, int]] = [self.entry]

        while self.stack:
            current_cell = self.stack[-1]
            if current_cell == self.exit:
                break
            available_neighbors = self._get_neighbors(current_cell)

            if available_neighbors:
                if self.exit in available_neighbors:
                    next_cell = self.exit
                else:
                    next_cell = available_neighbors [0]
                self.visited.add(next_cell)
                self.stack.append(next_cell)
            else:
                self.stack.pop()


    def _is_not_visited(self, neighbor: tuple[int, int]) -> bool:
        if neighbor in self.visited:
            return False
        return True

    def _is_wall_open(self, bit: int) -> bool:
        if bit:
            return False
        return True

    def _is_in_bounds(self, neighbor: tuple[int, int]) -> bool:
        x = neighbor[0]
        y = neighbor[1]
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def _is_available(self, wall: int, neighbor: tuple[int, int]) -> bool:
        if (
            self._is_in_bounds(neighbor)
            and self._is_wall_open(wall)
            and self._is_not_visited(neighbor)
            ):
            return True
        return False


    def _get_neighbors(self, current_cell: tuple[int, int]) -> list[tuple[int, int]]:
        key = current_cell
        value = self.cells[key]
        x = current_cell[0]
        y = current_cell[1]
        available_neighbors = []

        left = (value >> 3, -1, 0)
        down = ((value >> 2) % 2, 0, 1)
        right = ((value >> 1) % 2, 1, 0)
        up = (value % 2, 0, -1)
        moves = [left, down, right, up]

        for (wall, dx, dy) in moves:
            neighbor: tuple[int,int]= (x + dx, y + dy)
            if self._is_available(wall, neighbor):
                available_neighbors.append(neighbor)
        return available_neighbors
