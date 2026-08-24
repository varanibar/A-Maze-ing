class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: dict[tuple[int, int], int] = {}

        for x in range(self.width):
            for y in range(self.height):
                self.cells[(x, y)] = 15

    def to_hex_grid(self) -> str:
        lines = []

        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                cell_value = self.cells[(x, y)]
                row_str += f"{cell_value:x}"

            lines.append(row_str)

        return "\n".join(lines)

    def render(self) -> str:
        """Render the maze grid into a multi-line ASCII string representation.

        Scales the logical grid dimensions to canvas coordinates (2N + 1) to accommodate
        wall boundaries and corner posts:
        1. Initializes an internal 2D character array for wall slots and cell spaces.
        2. Places "+" posts at all even grid intersections.
        3. Reads each cell's bitmask to draw horizontal ("---") and vertical ("|") walls.
        4. Joins character rows with newlines.

        Returns:
            str: The formatted ASCII visual representation of the maze.
        """

        # 1. Scale dimensions to 2N + 1 to account for walls and intersection posts between cells
        grid_height = self.height * 2 + 1
        grid_width = self.width * 2 + 1

        # 2. Initialize blank canvas grid (cell centers get 3 spaces "   ", wall slots get " ")
        grid = []
        for grid_y in range(grid_height):
            row = []
            for grid_x in range(grid_width):
                if grid_x % 2 != 0:
                    row.append("   ") # Cell centers & horizontal wall slots
                else:
                    row.append(" ") # Post corners & vertical wall slots
            grid.append(row)

        # 3. Place "+" wall posts at all even intersection coordinates
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                grid[y * 2][x * 2] = "+"

        # 4. Draw remaining walls based on each cell's bitmask
        for (x, y), value in self.cells.items():
            # Translate logical cell (x, y) to text canvas coordinates
            grid_y = y * 2 + 1
            grid_x = x * 2 + 1

            # Bit 1 (1): North wall present -> draw horizontal wall above
            if value & 1:
                grid[grid_y - 1][grid_x] = "---"
            # Bit 2 (2): East wall present -> draw vertical wall right
            if value & 2:
                grid[grid_y][grid_x + 1] = "|"
            # Bit 3 (4): South wall present -> draw horizontal wall below
            if value & 4:
                grid[grid_y + 1][grid_x] = "---"
            # Bit 4 (8): West wall present -> draw vertical wall left
            if value & 8:
                grid[grid_y][grid_x - 1] = "|"

        # 5. Convert array rows into single formatted string
        lines = []
        for row in grid:
            lines.append("".join(row))

        return "\n".join(lines)

