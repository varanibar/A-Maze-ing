import curses
import ui.actions
import time
from parser import Config
from ui.maze_window import MazeWindow
from ui.menu_window import Menu
from ui.menu_window import MenuPanel
from maze_builder import build_maze
from maze_builder import MazeState

MENU_HEADER = "Actions:"

MAIN_ACTIONS: list[str] = [
    "Generate maze",
    "Quit"
    ]

MAZE_ACTIONS: list[str] = [
    "Solve",
    "Regenerate",
    "Change wall color",
    "Return",
    "Quit"
    ]

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


def validate_layout(
                    state: MazeState,
                    menu: Menu,
                    screen: curses.window
                    ) -> None:

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

    screen_h, screen_w = screen.getmaxyx()

    maze_panel_h, maze_panel_w = MenuPanel.calculate_size(menu)
    maze_window_h, maze_window_w = MazeWindow.calculate_size(state.maze_string)

    spacing = 2
    maze_window_border = 1

    required_screen_h = max(maze_panel_h, maze_window_h) + spacing * 2
    required_screen_w = maze_window_w + maze_panel_w + spacing * 3

    available_maze_h = screen_h - spacing * 2 - maze_window_border * 2
    available_maze_w = screen_w - maze_panel_w - spacing * 3 - maze_window_border * 2

    max_maze_input_h = (available_maze_h - 1) // 2
    max_maze_input_w = (available_maze_w - 1) // 4

    if required_screen_h > screen_h or required_screen_w > screen_w:

        message_1 = f"\nMaze:\n  Current size:                h = {state.config_data.height}   and    w = {state.config_data.width}\n"
        message_2 = f"  Max size for this terminal:  h = {max_maze_input_h}   and    w = {max_maze_input_w}\n"
        complete_message = message_1 + message_2

        raise ValueError(f"Terminal too small. Change terminal size or change maze dimensions.\n{complete_message}")


def initialize_display(
                screen: curses.window,
                ) -> None:

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


def run_main_screen(main_menu: Menu,
                    maze_menu: Menu,
                    state: MazeState,
                    screen: curses.window,
                    ) -> str:

    main_panel = MenuPanel(main_menu, "center", screen)

    while True:                                     # MAIN LOOP
        selection = main_panel.navigate_menu()
        main_panel.clear()

        if selection == "Generate maze":
            while True:                               # MAZE LOOP
                result = run_maze_screen(maze_menu, state, screen)

                if result == "Quit":
                    return "Quit"
                elif result == "Return":
                    break
                elif result == "Regenerate":
                    state = build_maze(state.config_file)
                    validate_layout(state, maze_menu, screen)
                    initialize_display(screen)
                    continue

        elif selection is None or selection == "Quit":
            ui.actions.quit_action(screen)
            return "Quit"


def run_maze_screen(
                    maze_menu: Menu,
                    state: MazeState,
                    screen: curses.window,
                    ) -> str:

    maze_panel = MenuPanel(maze_menu, "left", screen)
    maze_win = MazeWindow(maze_panel, state.maze_string, screen)

    while True:
        selection = maze_panel.navigate_menu()

        if selection == "Solve":
            pass
        elif selection == "Regenerate":
            return "Regenerate"
        elif selection == "Change wall color":
            ui.actions.change_color_action(maze_win)
            continue
        elif selection == "Return":
            ui.actions.return_action(maze_panel, screen)
            return "Return"
        elif selection is None or selection == "Quit":
            ui.actions.quit_action(screen)
            return "Quit"


def run_display(
                stdscr: curses.window,
                state: MazeState
                ) -> None:

    curses.curs_set(0)

    main_menu = Menu(MENU_HEADER, MAIN_ACTIONS)
    maze_menu = Menu(MENU_HEADER, MAZE_ACTIONS)

    validate_layout(state, maze_menu, stdscr)

    initialize_colors()
    initialize_display(stdscr)

    result = run_main_screen(main_menu, maze_menu, state, stdscr)
    if result == "Quit":
        return



def start_display(
                state: MazeState
                ) -> None:

    try:
        curses.wrapper(run_display, state)

    except ValueError as err:
        raise ValueError(f"{err}")


    """
    The wrapper:
    1. Starts curses
    2. Creates the main terminal window stdscr
    3. Calls the function run_display(stdscr: curses.window)
    4. Restores the terminal when run_display finishes or crashes.
    """
