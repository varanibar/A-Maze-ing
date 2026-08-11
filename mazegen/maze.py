'''
What it needs:
the width and the height from the config file
-Vero:
i will actually change it to the config_data so all the input is available
        to be able to merge the class Maze with MazeWindow and work on the actions
        of the Maze Menu

What it does:
-Creates the cells dict that represent the maze walls, these will be initially set to 15
    and later when the object is passed by the builder/generator, some of the walls of
    the cells will be opened and the maze is now contained in this dict.
-Once the maze is generated, now we need to represent thos bits in characters, this
    will be done with the render method that will return a string containing
    the characters that visually represent the cells of the maze

-Vero:
-I need to see how i can merge this class with the MazeWindow class
'''
class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: dict[tuple[int, int], int] = {}

        for x in range(self.width):
            for y in range(self.height):
                self.cells[(x, y)] = 15

    def render(self) -> str:
        grid_height = self.height * 2 + 1
        grid_width = self.width * 2 + 1

        grid = []
        for grid_y in range(grid_height):
            row = []
            for grid_x in range(grid_width):
                if grid_x % 2 != 0:
                    row.append("   ")
                else:
                    row.append(" ")
            grid.append(row)

        for y in range(self.height + 1):
            for x in range(self.width + 1):
                grid[y * 2][x * 2] = "+"

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

        lines = []
        for row in grid:
            lines.append("".join(row))

        return "\n".join(lines)
