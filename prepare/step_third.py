#coding:utf-8
import curses
import locale
locale.setlocale(locale.LC_ALL,'')
code = locale.getpreferredencoding()

def covert(string):
    uni_str = string.decode('utf-8')
    lenth = len(uni_str)
    return uni_str.encode(code),lenth

def line_resize(lines, width):
    count = len(lines)
    index = 0
    while index < count:
        line = lines[index].decode('utf-8')
        line_lenth = len(line)
        if line_lenth > width:
            s_width =  0
            while s_width < line_lenth:
                yield line[s_width:s_width+width].encode(code)
                s_width += width
            index += 1
        else:
            yield line.encode(code)
            index += 1

def main():
    stdscr = curses.initscr()
    curses.nocbreak()
    mode = NORMAL
    max_y, max_x = stdscr.getmaxyx()
    print_before, z = covert("输入一个文件地址:")
    stdscr.addstr((max_y-1)/2-1, (max_x-1-z)/2-1, print_before)
    stdscr.move((max_y-1)/2, (max_x-1-z)/2-1)
    path = stdscr.getstr()
    stdscr.move(0,0)
    stdscr.clear()
    stdscr.refresh()
    with open(path,'r') as f:
        lines = list(line_resize(f.readlines(), 5))
        for line in lines[-10:]:
            stdscr.addstr(line)
    while True:
        ch = stdscr.getch()
        if ch == 27:
            break

if __name__ == "__main__":
    NORMAL = 0
    INSERT = 1
    try:
        main()
    finally:
        curses.endwin()
