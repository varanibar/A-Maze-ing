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

    curses.curs_set(0)
    screen.bkgd(" ", curses.color_pair(1))
    screen.border()
    screen.addstr(1, x, text)
    screen.refresh()


class MenuWindow():
    def __init__(self, menu: list[str], y: int, x: int) -> None:
        self.menu = menu
        self.selected_row_idx = 0
        self.h, self.w = self.get_size()
        self.create_window(y, x)

    def get_size(self) -> tuple[int, int]:
        height: int = len(self.menu) + 4
        width: int = max(len(row) for row in self.menu) + 6
        return (height, width)

    def create_window(self, y: int, x: int) -> None:
        self.window = curses.newwin(self.h, self.w, y - self.h//2, x - self.w//2)
        self.window.bkgd(" ", curses.color_pair(1))
        self.window.keypad(True)
        self.window.border()
        self.window.refresh()

    def x_pos(self, text: str) -> int:
        x = self.w//2 - len(text)//2
        return x

    def print_menu(self) -> None:

        self.window.border()

        for idx, row in enumerate(self.menu):
            x = self.x_pos(row)
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

            if key == curses.KEY_UP and self.selected_row_idx > 0:
                self.selected_row_idx -= 1

            elif key == curses.KEY_DOWN and self.selected_row_idx < len(self.menu) - 1:
                self.selected_row_idx += 1

            elif key in (curses.KEY_ENTER, 10, 13):
                return self.menu[self.selected_row_idx]
                # self.window.clear()
                # text = f"You pressed {self.menu[self.selected_row_idx]}"
                # self.window.addstr(0, 1, text)
                # self.window.refresh()
                # if self.menu[self.selected_row_idx] == "Quit":
                #     text = "see ya! :("
                #     self.window.addstr(1, self.x_pos(text), text)
                #     self.window.refresh()
                #     time.sleep(2)
                #     sys.exit(0)
                # elif self.menu[self.selected_row_idx] == "Generate maze":
                #     break
                # else:
                #     self.window.getch()

            elif key in (curses.KEY_BACKSPACE, 127):
                return None

def handle_selection(menu: curses.window, selection: str, middle_y: int, middle_x: int):
    if selection == "Quit":
        text = "see ya!"
        menu.addstr(1, 1, text)
        menu.refresh()
        time.sleep(2)
        sys.exit(0)
    elif selection == "None":
        sys.exit(0)
    elif selection == "Generate maze":
        options_maze: list[str] = ["Solve", "Regenerate", "Write to file", "Return", "Quit"]
        maze_menu = MenuWindow(options_maze, middle_y//5, middle_x)
        selection = maze_menu.handle_user_input()
        maze_menu.window.clear()
        maze_menu.window.refresh()
        maze_menu.window.getch()

def run_display(stdscr: curses.window) -> None:
    initialize_colors()
    options_main_menu: list[str] = ["Generate maze", "Quit"]
    create_background(stdscr)
    y, x = stdscr.getmaxyx()
    middle_y = y//2
    middle_x = x//2
    main_menu = MenuWindow(options_main_menu, middle_y, middle_x)
    selection = main_menu.handle_user_input()
    main_menu.window.clear()
    main_menu.window.refresh()
    handle_selection(main_menu.window, selection, middle_y, middle_x)











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
