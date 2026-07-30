import curses

def main(screen: curses.window) -> None:
    curses.start_color()

    if curses.can_change_color():
        curses.init_color(10, 59, 106, 169)    #navy
        curses.init_color(11, 882, 682, 86)    #amber
        curses.init_pair(1, 11, 10)
    else:
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    STYLE = curses.color_pair(1)
    screen.bkgd(" ", STYLE)
    screen.clear()
    screen.addstr(1,40, "Welcome to A-Maze-ing!", STYLE)
    screen.box(10,10)
    screen.border()
    screen.refresh()
    screen.getch()


curses.wrapper(main)
