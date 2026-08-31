class Maze:
    """
    Represent a maze using a grid of cells encoded as wall bitmasks.

    Each cell is stored in a dictionary using its (x, y) coordinates as
    the key and an integer bitmask representing its walls as the value.
    Cells are initialized with all four walls present.
    """
    def __init__(self, width: int, height: int) -> None:
        """
        Initialize an empty maze with all cell walls closed.
        """
        self.width = width
        self.height = height
        self.cells: dict[tuple[int, int], int] = {}

        for x in range(self.width):
            for y in range(self.height):
                self.cells[(x, y)] = 15

    def to_hex_grid(self) -> str:
        """
        Convert the maze cell values into a hexadecimal grid.

        Returns:
            A multiline string containing the hexadecimal wall value
            of each cell.
        """
        lines = []

        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                cell_value = self.cells[(x, y)]
                row_str += f"{cell_value:x}"

            lines.append(row_str)

        return "\n".join(lines)

    def render(
        self,
        path_cells: set[tuple[int, int]] | None = None,
        entry: tuple[int, int] | None = None,
        exit: tuple[int, int] | None = None,
    ) -> str:
        """Render ASCII maze, optionally overlaying solution path
        and entry/exit markers."""

        # 1. Scale dimensions to 2N + 1 to account for walls and
        # intersection posts between cells
        grid_height = self.height * 2 + 1
        grid_width = self.width * 2 + 1

        # 2. Initialize blank canvas grid (cell centers get 3
        # spaces "   ", wall slots get " ")
        grid = []
        for grid_y in range(grid_height):
            row = []
            for grid_x in range(grid_width):
                if grid_x % 2 != 0:
                    row.append("   ")  # Cell centers & horizontal wall slots
                else:
                    row.append(" ")  # Post corners & vertical wall slots
            grid.append(row)

        # 3. Place "+" wall posts at all even intersection coordinates
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                grid[y * 2][x * 2] = "+"

        # 4. Draw remaining walls based on each cell's bitmask
        for (x, y), value in self.cells.items():
            grid_y = y * 2 + 1
            grid_x = x * 2 + 1

            if value & 1:
                grid[grid_y - 1][grid_x] = "---"
            if value & 2:
                grid[grid_y][grid_x + 1] = "|"
            if value & 4:
                grid[grid_y + 1][grid_x] = "---"
            if value & 8:
                grid[grid_y][grid_x - 1] = "|"

        # 5. Overlay solution path if provided
        if path_cells:
            for x, y in path_cells:
                grid_y = y * 2 + 1
                grid_x = x * 2 + 1
                grid[grid_y][grid_x] = " * "

        # 6. Mark entry and exit
        if entry:
            entry_x, entry_y = entry
            grid[entry_y * 2 + 1][entry_x * 2 + 1] = " E "

        if exit:
            exit_x, exit_y = exit
            grid[exit_y * 2 + 1][exit_x * 2 + 1] = " X "

        # 7. Convert array rows into single formatted string
        lines = []
        for row in grid:
            lines.append("".join(row))

        return "\n".join(lines)
