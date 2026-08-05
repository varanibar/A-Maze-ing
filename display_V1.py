import curses
import sys
import time


def initialize_style() -> int:
    # Stablishing style of the terminal
    curses.start_color()

    if curses.can_change_color():
        curses.init_color(10, 59, 106, 169)    #navy
        curses.init_color(11, 882, 682, 86)    #amber
        curses.init_pair(1, 11, 10)
    else:
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    return curses.color_pair(1)


class MenuBox():
    def __init__(self, options: list[str]) -> None:
        self.options = options
        self.height, self.width = self.get_size()
        self.style = initialize_style()

        # self.create_window()

    def get_size(self) -> tuple[int, int]:
        height: int = len(self.options) + 4
        width: int = max([len(row) for row in self.options]) + 6
        return (height, width)

    def create_window(self) -> None:
        self.box = curses.newwin(self.height, self.width, 0, 0)
        self.box.bkgd(" ", self.style)
        self.box.border()
        self.box.refresh()
        # self.box.getch()


def run_display(stdscr: curses.window) -> None:
    options: list[str] = ["Choose an option:", "g: Generate maze", "q: Quit program"]
    main_menu = MenuBox(options)
    main_menu.create_window()
    main_menu.box.getch()










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
