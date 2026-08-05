import curses
import sys
import time


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
    screen.addstr(1, x, text)
    curses.curs_set(0)
    screen.bkgd(" ", curses.color_pair(1))
    screen.border()
    screen.refresh()


def print_menu(window: curses.window, menu: list[str], selected_row_idx: int) -> None:
    h, w = window.getmaxyx()
    for idx, option in enumerate(menu):
        x = w//2 - len(option)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            window.addstr(y, x, option, curses.color_pair(2))
        else:
            window.addstr(y, x, option)
        window.refresh()


def handle_user_input(window: curses.window, menu: list[str]):
    selected_row_idx = 0
    print_menu(window, menu, selected_row_idx)
    while True:
        key = window.getch()
        window.clear()
        if key == curses.KEY_UP:
            window.addstr(1,0,"UP")
        elif key == curses.KEY_DOWN:
            window.addstr(1,0,"DOWN")
        elif key == curses.KEY_ENTER or key == 10:
            window.addstr(1,0,"ENTER")
        else:
            window.addstr(1,0, f"{key}")
        window.refresh()


class Window():
    def __init__(self, options: list[str], y: int, x: int) -> None:
        self.options = options
        self.h, self.w = self.get_size()
        self.create_window(y, x)

    def get_size(self) -> tuple[int, int]:
        height: int = len(self.options) + 4
        width: int = max([len(row) for row in self.options]) + 6
        return (height, width)

    def create_window(self, y , x) -> None:
        self.box = curses.newwin(self.h, self.w, y - self.h//2, x - self.w //2)
        self.box.bkgd(" ", curses.color_pair(1))
        self.box.keypad(True)
        self.box.border()
        self.box.refresh()


def run_display(stdscr: curses.window) -> None:
    initialize_colors()
    options: list[str] = ["Generate maze", "Quit"]
    create_background(stdscr)
    y, x = stdscr.getmaxyx()
    middle_y = y//2
    middle_x = x//2
    main_menu = Window(options, middle_y, middle_x)
    # print_menu(main_menu.box, options, 1)
    # time.sleep(2)
    handle_user_input(main_menu.box, options)
    # options_maze: list[str] = ["Solve", "Regenerate", "Write to file", "Return", "Quit"]
    # maze_menu = Window(options_maze, middle_y, middle_x)
    # print_menu(maze_menu.box, options_maze)
    # handle_user_input(maze_menu.box)
    # maze_window.box.getch()










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
