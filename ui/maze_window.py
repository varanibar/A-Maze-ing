import curses
import time
from ui.menu_window import MenuPanel


class MazeWindow():

    def __init__(
            self,
            maze_panel: MenuPanel,
            maze_string: str,
            screen: curses.window
            ) -> None:

        self.h, self.w = self.calculate_size(maze_string)
        self.top, self.left, self.right = self.calculate_position(maze_panel, screen)
        self.maze_string = maze_string
        self.color_style = curses.color_pair(1)
        self.create_window()
        self.print_maze()

    @staticmethod
    def calculate_size(
                    maze_string: str,
                    ) -> tuple[int, int]:

        maze_window_border = 1
        maze_rows = maze_string.splitlines()

        maze_window_h = len(maze_rows) + maze_window_border * 2
        maze_window_w = max(len(line) for line in maze_rows) + maze_window_border * 2

        return (maze_window_h, maze_window_w)

    def calculate_position(
                        self,
                        maze_panel: MenuPanel,
                        screen: curses.window
                        ) -> tuple[int, int, int]:

        screen_h, screen_w = screen.getmaxyx()
        padding = 1

        top = screen_h//2 - self.h//2
        left = maze_panel.right + screen_w//2 - maze_panel.right//2 - self.w//2 - padding
        right = left + self.w

        if (
            top < 0
            or left < 0
            or right > screen_w
            or top + self.h > screen_h
            or left + self.w > screen_w
            or right + padding > screen_w
            ):
            raise ValueError(f"Limits surpassed")

        else:
            return (top, left, right)

    def create_window(
                    self
                    ) -> None:

        self.window = curses.newwin(self.h, self.w, self.top, self.left)

        self.window.bkgd(" ", curses.color_pair(1))
        self.window.keypad(True)
        self.window.border()
        self.window.refresh()

    def print_maze(
                self
                ) -> None:

        maze_lines = self.maze_string.splitlines()

        for y, line in enumerate(maze_lines):
            self.window.addstr(y + 1, 1, line, self.color_style)

        self.window.refresh()

