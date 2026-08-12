import time
import curses
from typing import Literal
from parser import Config
import menu_actions
from maze_window import MazeWindow
from menu_window import Menu
from menu_window import MenuPanel

MenuPosition = Literal["center", "left"]


def initialize_colors(
                    ) -> None:

    curses.start_color()

    if curses.can_change_color():
        curses.init_color(10, 59, 106, 169)
        curses.init_color(11, 882, 682, 86)
        curses.init_pair(1, 11, 10)
        curses.init_pair(2, 10, 11)

    else:
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)


def create_background(
                    screen: curses.window
                    ) -> None:

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


def validating_terminal_size(
                            config_data: Config,
                            maze_string: str,
                            header: str,
                            actions: list[str],
                            screen: curses.window
                            ) -> None:

    screen_h, screen_w = screen.getmaxyx()

    maze_panel_h, maze_panel_w = MenuPanel.calculate_size(header, actions)
    maze_window_h, maze_window_w = MazeWindow.calculate_size(maze_string)

    spacing = 2
    maze_window_border = 1

    required_screen_h = max(maze_panel_h, maze_window_h) + spacing * 2
    required_screen_w = maze_window_w + maze_panel_w + spacing * 3

    available_maze_h = screen_h - spacing * 2 - maze_window_border * 2
    available_maze_w = screen_w - maze_panel_w - spacing * 3 - maze_window_border * 2

    max_maze_input_h = (available_maze_h - 1) // 2
    max_maze_input_w = (available_maze_w - 1) // 4

    if required_screen_h > screen_h or required_screen_w > screen_w:

        message_1 = f"\nMaze:\n  Current size:                h = {config_data.height}   and    w = {config_data.width}\n"
        message_2 = f"  Max size for this terminal:  h = {max_maze_input_h}   and    w = {max_maze_input_w}\n"
        complete_message = message_1 + message_2

        raise ValueError(f"Terminal too small. Change terminal size or change maze dimensions.\n{complete_message}")


def run_display(
                stdscr: curses.window,
                config_data: Config,
                maze_string: str
                ) -> None:

    header = "Actions:"

    main_actions: list[str] = [
        "Generate maze",
        "Quit"
        ]

    maze_actions: list[str] = [
        "Solve",
        "Regenerate",
        "Change wall color",
        "Return",
        "Quit"
        ]

    '''
    1. Maze logical size
   width = number of maze cells
    each maze cell takes 4 terminal columns horizontally
   height = number of maze cells
    each cell takes 2 terminal rows vertically

    2. Renderer grid size
    grid_width = width * 2 + 1
    grid_height = height * 2 + 1

    3. Actual curses/terminal size
    rendered_width = width * 4 + 1
        number of terminal columns
    rendered_height = height * 2 + 1
        number of terminal rows
    '''

    validating_terminal_size(config_data, maze_string, header, maze_actions, stdscr)
    initialize_colors()
    create_background(stdscr)

    main_menu = Menu(header, main_actions)
    main_panel = MenuPanel(main_menu, "center", stdscr)

    while True:
        selection = main_panel.handle_user_input()

        main_panel.clear()
        color_style = curses.color_pair(1)

        if selection is None or selection == "Quit":
            menu_actions.quit_action(stdscr)
            return

        if selection == "Generate maze":
            maze_menu = Menu(header, maze_actions)
            maze_panel = MenuPanel(maze_menu, "left", stdscr)

            maze_win = MazeWindow(maze_panel, maze_string, color_style, stdscr)

            while True:
                maze_selection = maze_panel.handle_user_input()

                if maze_selection == "Solve":
                    pass
                elif maze_selection == "Regenerate":
                    pass
                elif maze_selection == "Change wall color":
                    menu_actions.change_color_action(maze_win)
                    pass
                elif maze_selection == "Return":
                    menu_actions.return_action(stdscr, maze_panel.window)
                    break
                elif maze_selection is None or maze_selection == "Quit":
                    menu_actions.quit_action(stdscr)
                    return


def start_display(
                config_data: Config,
                maze_string: str
                ) -> None:

    try:
        curses.wrapper(run_display, config_data, maze_string)

    except ValueError as err:
        raise ValueError(f"{err}")


    """
    The wrapper:
    1. Starts curses
    2. Creates the main terminal window stdscr
    3. Calls the function run_display(stdscr: curses.window)
    4. Restores the terminal when run_display finishes or crashes.
    """
