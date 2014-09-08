import curses
from curses.textpad import Textbox

def main():
    stdscr = curses.initscr()
    curses.cbreak()
    curses.curs_set(0)
    size_y,size_x = stdscr.getmaxyx()
    
    # curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    # curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.nodelay(1)
    stdscr.hline(size_y-2,0,ord('-'),size_x)
    stdscr.move(size_y-1,0)
    content = []
    line = ""
    # input_y, input_x = size_y-3,0
    while True:
        ch = stdscr.getch()
        if ch == -1:
            continue
        elif ch == curses.KEY_ENTER or ch == 10:
            stdscr.clear()
            stdscr.hline(size_y-2,0,ord('-'),size_x)
            stdscr.refresh()
            content.append(line)
            line = ""
            show_content(stdscr, content)
            stdscr.move(size_y-1,0)
        else:
            line += chr(ch)

def show_content(stdscr, content):
    stdscr.move(0,0)
    for y in xrange(len(content)):
        stdscr.addstr(y,0,content[y])

if __name__ == "__main__":
    try:
        main()
    finally:
        curses.endwin()
