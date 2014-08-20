# coding:utf-8
import curses
import locale
from util import covert, line_resize, parse

class UI(object):
    def __init__(self):
        locale.setlocale(locale.LC_ALL,'')
        self.code = locale.getpreferredencoding()
        self.mode = 0
        self.content = []

    def start(self):
        self.stdscr = curses.initscr()
        self.scr_y, self.scr_x = self.stdscr.getmaxyx()
        self._draw_line()
        self._insert_loop()

    def end(self):
        curses.endwin()

    def _draw_line(self):
        self.stdscr.hline(self.scr_y-2,0,ord('-'),self.scr_x)

    def clear(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        self._draw_line()

    def draw_screen(self):
        lines = list(line_resize(self.content, self.scr_x, self.code))
        self.stdscr.move(0,0)
        y = 0
        for line in lines[-(self.scr_y-3):]:
           self.stdscr.addstr(covert(line, self.code)[0])
           y += 1
           self.stdscr.move(y,0)

    def draw_inputArea(self, line, y, x):
        self.stdscr.move(y,0)
        self.stdscr.clrtoeol()
        self.refresh()
        self.stdscr.addstr(line)
        self.stdscr.move(y,x)

    def check_pos(self, type_, value):
        y, x = self.stdscr.getmaxyx()
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

    def _insert_loop(self):
        curses.noecho()
        curses.cbreak()
        line = ""
        self.stdscr.move(self.scr_y-1,0)
        while self.mode == 0:
            ch = self.stdscr.getch()
            # KEY_Enter
            if ch == 10 :
                self.stdscr.clear()
                self.stdscr.refresh()
                self.content.append(line)
                line = ""
                self.draw_screen()
                self._draw_line()
                self.stdscr.move(self.scr_y-1,0)
            # KEY_Esc
            elif ch == 27:
                self.mode = 1
                line = ''
                self.stdscr.move(self.scr_y-1,0)
                self.stdscr.clrtoeol()
                self.stdscr.refresh()
            # KEY_Backspace
            elif ch == 127:
                y,x = curses.getsyx()
                line = line[:-1]
                self.draw_inputArea(line, y, x-1)
            else:
                if ch < 256:
                    string = chr(ch)
                else:
                    string = parse(ch)
                self.stdscr.addstr(string)
                line += string
        self._normal_loop()

    def _normal_loop(self):
        curses.cbreak()
        curses.noecho()
        pos_y,pos_x = curses.getsyx()
        move = self.stdscr.move
        while self.mode == 1:
            ch = self.stdscr.getch()
            if ch == curses.KEY_UP or ch == ord('k'):
                pos_y = self.check_pos('y',pos_y - 1)
                move(pos_y, pos_x)
            elif ch == curses.KEY_DOWN or ch == ord('j'):
                pos_y = self.check_pos('y',pos_y + 1)
                move(pos_y, pos_x)
            elif ch == curses.KEY_LEFT or ch == ord('h'):
                pos_x = self.check_pos('x',pos_x - 1)
                move(pos_y, pos_x)
            elif ch == curses.KEY_RIGHT or ch == ord('l'):
                pos_x = self.check_pos('x',pos_x + 1)
                move(pos_y, pos_x)
            elif ch == ord('i'):
                self.mode = 0
        self._insert_loop()

if __name__ == "__main__":
    try:
        ui = UI()
        ui.start()
    finally:
        ui.end()
