import curses
import time
import sys
from typing import Literal


MenuPosition = Literal["center", "left"]


def initialize_colors() -> None:
    curses.start_color()

    if curses.can_change_color():
        curses.init_color(10, 59, 106, 169)
        curses.init_color(11, 882, 682, 86)
        curses.init_pair(1, 11, 10)
        curses.init_pair(2, 10, 11)
    else:
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)


def create_background(screen: curses.window) -> None:
    h, w = screen.getmaxyx()
    text_top = "Welcome to A-Maze-ing!"
    text_bottom = "Project made by varaniba and pride-ol"
    x_text_top = w//2 - len(text_top)//2
    x_text_bottom = w//2 - len(text_bottom)//2

    curses.curs_set(0)
    screen.bkgd(" ", curses.color_pair(1))
    screen.border()
    screen.addstr(0, x_text_top, text_top)
    screen.addstr(h - 1, x_text_bottom, text_bottom)
    screen.refresh()


class MenuWindow():
    def __init__(
            self,
            menu: list[str],
            position: MenuPosition,
            screen: curses.window
            ) -> None:

        self.menu = menu
        self.position = position
        self.selected_row_idx = 1
        self.h, self.w = self.calculate_size(menu)
        self.top, self.left, self.right = self.calculate_position(screen)
        self.create_window()

    @staticmethod
    def calculate_size(menu: list[str]) -> tuple[int, int]:
        inner_padding = 4
        height: int = len(menu) + inner_padding
        width: int = max(len(row) for row in menu) + inner_padding + inner_padding//2
        return (height, width)

    def calculate_position(self, screen: curses.window) -> tuple[int, int, int]:
        screen_h, screen_w = screen.getmaxyx()
        padding = 2

        if self.position == "center":
            top = screen_h//2 - self.h//2
            left = screen_w//2 - self.w//2
            right = screen_w//2 + self.w//2

        elif self.position == "left":
            top = screen_h//2 - self.h//2
            left = padding
            right = left + self.w

        if (
            top < 0
            or left < 0
            or right > screen_w
            or top + self.h > screen_h
            or left + self.w > screen_w
            or right + padding > screen_w
            ):
            raise ValueError("Terminal is too small to display the program")
        else:
            return (top, left, right)

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

class MazeWindow():
    def __init__(self, maze_h: int, maze_w: int, maze_menu: curses.window, screen: curses.window) -> None:
        self.h = maze_h
        self.w = maze_w
        self.top, self.left, self.right = self.calculate_position(maze_menu, screen)
        self.create_window()

    def calculate_position(self, maze_menu: curses.window, screen: curses.window) -> tuple[int, int, int]:
        screen_h, screen_w = screen.getmaxyx()
        padding = 1

        top = screen_h//2 - self.h//2
        left = maze_menu.right + screen_w//2 - maze_menu.right//2 - self.w//2 - padding
        right = left + self.w
        if (
            top < 0
            or left < 0
            or right > screen_w
            or top + self.h > screen_h
            or left + self.w > screen_w
            or right + padding > screen_w
            ):
            message = f"top = {top} < 0\nor left = {left} < 0\nor right = {right} > screen_w = {screen_w}\nor top = {top} + h= {self.h} >  screen_h = {screen_h}\nor  left = {left} + w = {self.w }> screen_w = {screen_w}\nor right = {right} + padding = {padding} > screen_w = {screen_w}"
            raise ValueError(f"Limits surpassed\n{message}")
        else:
            return (top, left, right)

    def create_window(self) -> None:
        self.window = curses.newwin(self.h, self.w, self.top, self.left)

        self.window.bkgd(" ", curses.color_pair(1))
        self.window.keypad(True)
        self.window.border()
        self.window.addstr(1, 1, f"h = {self.h}")
        self.window.addstr(2, 1, f"w = {self.w}")

        self.window.refresh()

def quit_action(stdscr: curses.window) -> None:
    text = "see ya!"
    y, x = stdscr.getmaxyx()

    stdscr.clear()
    stdscr.bkgd(" ", curses.color_pair(1))
    stdscr.border()
    stdscr.addstr(y // 2, x // 2 - len(text) // 2, text)
    stdscr.refresh()

    time.sleep(1)

def validating_terminal_size(screen: curses.window,  maze_opt: list[str], maze_h: int, maze_w: int):
    screen_h, screen_w = screen.getmaxyx()
    maze_menu_h, maze_menu_w = MenuWindow.calculate_size(maze_opt)
    outer_padding = 2

    required_h = maze_h + outer_padding
    required_w = maze_w + outer_padding * 2 + maze_menu_w + 1
    max_maze_h = screen_h - outer_padding
    max_maze_w = screen_w - outer_padding * 2 - maze_menu_w - 1

    if required_h > screen_h or required_w > screen_w:

        message_1 = f"\nTerminal:\n  Current size:   h = {screen_h}   and    w = {screen_w}\n"
        message_2 = f"  Required size:  h = {required_h}   and    w = {required_w}"

        message_3 = f"\nMaze:\n  Current size:                h = {maze_h}   and    w = {maze_w}\n"
        message_4 = f"  Max size for this terminal:  h = {max_maze_h}   and    w = {max_maze_w}\n"
        complete_message = message_1 + message_2 + message_3 + message_4

        raise ValueError(f"Terminal too small. Change terminal size or change maze dimensions.\n{complete_message}")


def run_display(stdscr: curses.window) -> None:
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

    # maze_h, maze_w = (70, 270)
    maze_h, maze_w = (70, 101)
    validating_terminal_size(stdscr, maze_opt, maze_h, maze_w)
    initialize_colors()
    create_background(stdscr)

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
            maze = MazeWindow(maze_h, maze_w, maze_menu, stdscr)
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

def start_display() -> None:
    try:
        curses.wrapper(run_display)
    except ValueError as err:
        print(f"Caught {err.__class__.__name__}: {err}")



    """
    Python executes a module's top-level code from top to bottom when the file
    is imported. This guard ensures that curses starts only when this file is
    run directly, not when its classes or functions are imported elsewhere.
    """


if __name__ == "__main__":
    start_display()

    """
    The wrapper:
    1. Starts curses
    2. Creates the main terminal window stdscr
    3. Calls the function run_display(stdscr: curses.window)
    4. Restores the terminal when run_display finishes or crashes.
    """
