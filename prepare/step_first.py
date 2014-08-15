import curses

def main(win):
    global stdscr
    stdscr = win

    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    current_x = 0
    current_y = 2
    while True:
        y,x = stdscr.getmaxyx()
        stdscr.attrset(curses.color_pair(1))
        stdscr.addstr(0,0,"hello world")
        stdscr.attrset(curses.color_pair(2))
        stdscr.addstr(1,0,"good luck")
        ch = stdscr.getch()
        if ch == ord('q') or ch == ord('Q'):
            return
        else:
            stdscr.addstr(10,0,str(x))
            stdscr.addstr(10,6,str(y))
            temp = current_x+1
            if temp % x == 0:
                stdscr.addch(current_y,current_x,ch)
                stdscr.addstr(10,10,str(current_x))
                current_y += 1
                current_x = 0
            else:
                stdscr.addch(current_y,current_x,ch)
                current_x += 1

curses.wrapper(main)
