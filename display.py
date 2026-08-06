import curses
import time
from typing import Literal

MenuPosition = Literal ["top", "center", "left"]

def initialize_colors() -> None:
    # Stablishing style of the terminal
    curses.start_color()

    if curses.can_change_color():
        curses.init_color(10, 59, 106, 169)    #navy
        curses.init_color(11, 882, 682, 86)    #amber
        curses.init_pair(1, 11, 10)
        curses.init_pair(2, 10, 11)
    else:
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)


def create_background(screen: curses.window) -> None:
    h, w = screen.getmaxyx()
    text = "Welcome to A-Maze-ing!"
    x = w//2 - len(text)//2

    curses.curs_set(0)
    screen.bkgd(" ", curses.color_pair(1))
    screen.border()
    screen.addstr(1, x, text)
    screen.refresh()


class MenuWindow():
    def __init__(self, menu: list[str], position: MenuPosition, screen: curses.window) -> None:
        self.menu = menu
        self.position = position
        self.selected_row_idx = 1
        self.h, self.w = self.get_size()
        self.top, self.left = self.calculate_position(screen)
        self.create_window()

    def get_size(self) -> tuple[int, int]:
        height: int = len(self.menu) + 4
        width: int = max(len(row) for row in self.menu) + 6
        return (height, width)

    def calculate_position(self, screen: curses.window) -> tuple[int, int]:
        y,x = screen.getmaxyx()
        if self.position == "center":
            top = y//2 - self.h//2
            left = x//2 - self.w//2
        elif self.position == "top":
            top = 2
            left = x//2 - self.w//2
        elif self.position == "left":
            top = y//2 - self.h//2
            left = 2
        return (top, left)

    def create_window(self) -> None:
        self.window = curses.newwin(self.h, self.w, self.top, self.left)
        self.window.bkgd(" ", curses.color_pair(1))
        self.window.keypad(True)
        self.window.border()
        self.window.refresh()


    def print_menu(self) -> None:

        self.window.border()

        for idx, row in enumerate(self.menu):
            x = self.w//2 - len(row)//2
            y = self.h//2 - len(self.menu)//2 + idx
            if idx == self.selected_row_idx:
                self.window.addstr(y, x, row, curses.color_pair(2))
            else:
                self.window.addstr(y, x, row)

        self.window.refresh()

    def handle_user_input(self) -> str | None:
        while True:
            self.window.clear()
            self.print_menu()

            key = self.window.getch()

            if key == curses.KEY_UP and self.selected_row_idx > 1:
                self.selected_row_idx -= 1

            elif key == curses.KEY_DOWN and self.selected_row_idx < len(self.menu) - 1:
                self.selected_row_idx += 1

            elif key in (curses.KEY_ENTER, 10, 13):
                return self.menu[self.selected_row_idx]

            elif key == 27:
                return None


def quit_action(stdscr: curses.window) -> None:
    text = "see ya!"
    y, x = stdscr.getmaxyx()

    stdscr.clear()
    stdscr.bkgd(" ", curses.color_pair(1))
    stdscr.border()
    stdscr.addstr(y // 2, x // 2 - len(text) // 2, text)
    stdscr.refresh()

    time.sleep(1)

def run_display(stdscr: curses.window) -> None:
    initialize_colors()
    create_background(stdscr)

    main_opt: list[str] = [
        "Actions:",
        "Generate maze",
        "Quit"
        ]

    maze_opt: list[str] = [
    "Actions:",
    "Solve",
    "Regenerate",
    "Write to file",
    "Return",
    "Quit"
    ]

    main_menu = MenuWindow(main_opt, "center", stdscr)
    while True:
        main_selection = main_menu.handle_user_input()
        main_menu.window.clear()
        main_menu.window.refresh()

        if main_selection is None or main_selection == "Quit":
            quit_action(stdscr)
            return

        if main_selection == "Generate maze":
            maze_menu = MenuWindow(maze_opt, "left", stdscr)
            while True:
                maze_selection = maze_menu.handle_user_input()

                if maze_selection == "Solve":
                    pass
                elif maze_selection == "Regenerate":
                    pass
                elif maze_selection == "Write to file":
                    pass
                elif maze_selection == "Return":
                    maze_menu.window.clear()
                    maze_menu.window.refresh()
                    del maze_menu
                    stdscr.touchwin()
                    stdscr.refresh()
                    break
                elif maze_selection is None or maze_selection == "Quit":
                    quit_action(stdscr)
                    return











    """
    Python executes a module's top-level code from top to bottom when the file
    is imported. This guard ensures that curses starts only when this file is
    run directly, not when its classes or functions are imported elsewhere.
    """
if __name__ == "__main__":
    curses.wrapper(run_display)

    """
    The wrapper:
    1. Starts curses
    2. Creates the main terminal window stdscr
    3. Calls the function run_display(stdscr: curses.window)
    4. Restores the terminal when run_display finishes or crashes.
    """

# def main(screen: curses.window):
#     screen.border()
#     screen.refresh()
#     time.sleep(0.5)
#     menu_box = curses.newwin(10, 30, 0,0)
#     menu_box.border()
#     menu_box.refresh()
#     menu_box.getch()
