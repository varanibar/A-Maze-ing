import curses
from ui.maze_window import MazeWindow
from maze_builder import MazeState

def draw_maze_coordinates(maze_win: MazeWindow, screen: curses.window) -> None:

    cell_h = maze_win.CELL_H
    cell_w = maze_win.CELL_W
    top = maze_win.top
    left = maze_win.left
    right = maze_win.right
    grid_h = maze_win.h - cell_h - 1
    grid_w = maze_win.w - cell_w - 1
    axis_x = left + 2
    axis_y = top + 1
    height = grid_h//cell_h
    width = grid_w//cell_w
    dx = 0
    step = 1

    if width > 15:
        step = 2

    for column in range(0, grid_w + 1, cell_w):
        cell = column//cell_w
        if cell % step == 0:
            if cell >= 10:
                dx = 1
            screen.addstr(top - 1, axis_x + column - dx, str(cell))
    screen.addstr(top - 1, axis_x + column - dx, str(cell))

    step = 1
    if height > 15:
        step = 2

    for row in range (0, grid_h + 1, cell_h):
        cell = row//cell_h
        if cell % step == 0:
            screen.addstr(axis_y + row, right + 1, str(cell))
    screen.addstr(axis_y + row, right + 1, str(cell))
    screen.refresh()

def draw_42_hint(state: MazeState, screen: curses.window) -> None:
    if not state.reserved_cells:
        lines = [
            "Looking for this?",
            "",
            "   4  4   22 ",
            "   4  4  2  2",
            "   4444    2 ",
            "      4   2  ",
            "      4  2222",
            "",
            "Make the maze bigger or "
            "move the entry and exit outside"
            " the pattern to see the 42 hint!",
        ]

        screen_h, screen_w = screen.getmaxyx()

        start_y = screen_h - len(lines) - 2
        start_x = 2

        for i, line in enumerate(lines):
            try:
                screen.addstr(start_y + i, start_x, line)
            except curses.error:
                pass

        screen.refresh()



