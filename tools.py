#coding: utf-8

__all__ = ['covert','line_resize','parse','draw_line','draw_screen','move','draw_input','check_pos']

import locale
locale.setlocale(locale.LC_ALL,'')
code = locale.getpreferredencoding()

def covert(string,code):
    new_string = string.decode('utf-8')
    lenth = len(new_string)
    return new_string.encode(code), lenth

def line_resize(lines, width, code):
    count = len(lines)
    index = 0
    while index < count:
        line = lines[index].decode('utf-8')
        line_lenth = len(line)
        if line_lenth > width:
            s_width = 0
            while s_width < line_lenth:
                yield line[s_width:s_width+width].encode(code)
                s_width += width
            index += 1
        else:
            yield line.encode(code)
            index += 1

def combine(func):
    def wrapper(*args, **kwargs):
        value = "".join(reversed(list(func(*args, **kwargs))))
        return value
    return wrapper

@combine
def parse(value):
    while value:
        ch = value % 1000
        value /= 1000
        yield chr(ch)

def draw_line(stdscr, y, x):
    stdscr.hline(y,0,ord('-'),x)

def move(stdscr, y, x):
    stdscr.move(y,x)

def draw_screen(stdscr, content, hight, width):
    lines = list(line_resize(content, width, code))
    move(stdscr,0,0)
    y = 0
    for line in lines[-hight:]:
        stdscr.addstr(covert(line,code)[0])
        y += 1
        move(stdscr, y, 0)

def draw_input(stdscr, line, y, x):
    move(stdscr, y,0)
    stdscr.clrtoeol()
    self.refresh()
    stdscr.addstr(line)
    move(stdscr,y,x)

def check_pos(stdscr, type_, value):
    y, x = stdscr.getmaxyx()
    if type_ == 'x':
        if value < 0:
            value = 0
        if value > x-1:
            value = x-1
    if type_ == 'y':
        if value < 0:
            value = 0
        if value > y-1:
            value = y-1
    return value

