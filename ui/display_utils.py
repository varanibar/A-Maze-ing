# Built-in modules
import curses

# Project modules
from maze_builder import MazeState
from ui.maze_window import MazeWindow


def initialize_colors(
                    ) -> None:
    """Initialize the color pairs used by the curses interface.

    Uses custom colors when supported by the terminal and falls back
    to standard curses colors otherwise.
    """

    curses.start_color()

    if curses.can_change_color():
        curses.init_color(10, 59, 106, 169)
        curses.init_color(11, 882, 682, 86)
        curses.init_pair(1, 11, 10)
        curses.init_pair(2, 10, 11)

    else:
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)


def initialize_display(
                    screen: curses.window,
                    ) -> None:
    """Draw the main screen background, border, and project titles."""

    h, w = screen.getmaxyx()

    text_top = "Welcome to A-Maze-ing!"
    text_bottom = "Project made by varaniba and pride-ol"
    x_text_top = w//2 - len(text_top)//2
    x_text_bottom = w//2 - len(text_bottom)//2

    screen.clear()
    screen.bkgd(" ", curses.color_pair(1))
    screen.border()
    screen.addstr(0, x_text_top, text_top)
    screen.addstr(h - 1, x_text_bottom, text_bottom)
    screen.refresh()


def draw_maze_coordinates(
                        maze_win: MazeWindow,
                        screen: curses.window
                        ) -> None:
    """Draw the coordinates of the maze's cells next to the maze window."""

    cell_h = maze_win.CELL_H
    cell_w = maze_win.CELL_W

    top = maze_win.top
    left = maze_win.left
    right = maze_win.right

    grid_h = maze_win.h - cell_h - 1
    grid_w = maze_win.w - cell_w - 1
    start_x = left + cell_w
    start_y = top + cell_h

    dx = 0
    step = 1

    for column in range(0, grid_w, cell_w):
        cell = column//cell_w
        if cell % step == 0:
            if cell >= 10:
                dx = 1
            screen.addstr(top - 1, start_x + column - dx, str(cell))

    for row in range(0, grid_h, cell_h):
        cell = row//cell_h
        if cell % step == 0:
            screen.addstr(start_y + row, right + 1, str(cell))

    screen.refresh()


def draw_42_hint(
                state: MazeState,
                screen: curses.window
                ) -> None:
    """Draw a small hint about the hidden 42 pattern."""

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
            " the pattern to see the 42 pattern!",
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
