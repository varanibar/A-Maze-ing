import random
import time
import curses
from maze_window import MazeWindow


def quit_action(
                stdscr: curses.window
                ) -> None:

    text = "see ya!"
    y, x = stdscr.getmaxyx()

    stdscr.clear()
    stdscr.bkgd(" ", curses.color_pair(1))
    stdscr.border()
    stdscr.addstr(y // 2, x // 2 - len(text) // 2, text)
    stdscr.refresh()

    time.sleep(1)


def return_action(
                stdscr: curses.window,
                window: curses.window
                ) -> None:

    window.clear()
    window.refresh()
    del window

    stdscr.touchwin()
    stdscr.refresh()


def change_color_action(
                    maze_win: MazeWindow
                    ) -> None:

    foreground, background = curses.pair_content(1)

    colors = [
        curses.COLOR_RED,
        curses.COLOR_GREEN,
        curses.COLOR_YELLOW,
        curses.COLOR_MAGENTA,
        curses.COLOR_CYAN,
        curses.COLOR_WHITE,
        ]

    if foreground in colors:
        colors.remove(foreground)
    new_foreground = random.choice(colors)
    curses.init_pair(3, new_foreground, background)

    maze_win.color_style = curses.color_pair(3)
    maze_win.print_maze()

