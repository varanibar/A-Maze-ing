import curses
import sys
import time

class Display():
    def __init__(self):
        pass

    def menu_styling(self) -> int:
        # Stablishing style of the terminal
        curses.start_color()

        if curses.can_change_color():
            curses.init_color(10, 59, 106, 169)    #navy
            curses.init_color(11, 882, 682, 86)    #amber
            curses.init_pair(1, 11, 10)
        else:
            curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        return curses.color_pair(1)


class MenuBox(Display):
    # Class representating the terminal menu interface
    def __init__(self, screen: curses.window, options: list) -> None:
        self.options = options
        self.box_height, self.box_width = self.get_box_size()
        self.style = super().menu_styling()
        self.menu_building(screen)

    def menu_building(self, screen: curses.window) -> None:
        try:
            self.checking_dimensions(screen)
        except Exception as err:
            curses.endwin()
            print(f"Caught {err.__class__.__name__}: {err}")
            sys.exit(0)
        else:
            self.box.border()
            self.box.bkgd(" ", self.style)
            self.writing_options()
            self.box.refresh()
            self.box.getch()

    def checking_dimensions(self, screen: curses.window) -> None:
        y, x = screen.getmaxyx()
        needed_y = self.box_height
        needed_x = self.box_width
        if needed_y > y or needed_x > x:
            raise Exception("Terminal size too small, try resizing it.")
        else:
            self.box = curses.newwin(needed_y, needed_x, int(y/2), int((x - needed_x)/2 - 0.5))

    def get_box_size(self) -> tuple[int, int]:
        needed_y = len(self.options) + 4
        needed_x = max([len(item) for item in self.options]) + 4
        return (needed_y, needed_x)

    def writing_options(self) -> None:
        y, x = self.box.getmaxyx()
        position_y = 1
        for item in self.options:
            position_y += 1
            position_x = 2
            self.box.addstr(position_y, position_x, item)


class MainScreen(Display):
    def __init__(self, screen: curses.window):
        self.screen = screen
        self.style = super().menu_styling()
        self.screen.bkgd(" ", self.style)
        self.screen.border()
        y, x = self.screen.getmaxyx()
        title: str= "welcome to A-Maze-ing!"
        position_y = int(y / 4)
        position_x = int((x - len(title))/2 - 0.5)
        self.screen.addstr(position_y, position_x, title)
        self.screen.refresh()
        time.sleep(1)

def main(stdscr: curses.window):
    screen = MainScreen(stdscr)
    options_main_menu: list[str] = ["Choose an option:", "", "g: Generate maze", "q: Quit program"]
    main_menu = MenuBox(stdscr, options_main_menu)
    stdscr.clear()
    options_maze_menu: list[str] = ["g: Generate maze"]
    maze_menu = MenuBox(stdscr, options_maze_menu)

# def main(screen: curses.window):
#     screen.border()
#     screen.refresh()
#     time.sleep(0.5)
#     menu_box = curses.newwin(10, 30, 0,0)
#     menu_box.border()
#     menu_box.refresh()
#     menu_box.getch()

curses.wrapper(main)
