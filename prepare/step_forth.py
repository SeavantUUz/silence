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
        self._insert_loop()

    def end(self):
        curses.endwin()

    def getyx(self):
        self.scr_y, self.scr_x = self.stdscr.getmaxyx()

    def clear(self):
        self.stdscr.clear()
        self.stdscr.refresh()

    def draw_screen(self):
        pass

    def draw_inputArea(self):
        pass

    def check_pos(self, type_, value):
        pass

    def clear_input(self):
        pass

    def _insert_loop(self):
        curses.noecho()
        curses.cbreak()
        line = ""
        while self.mode == 0:
            ch = stdscr.getch()
            if ch == curses.KEY_ENTER:
                self.stdscr.clear()
                stdscr.hline(self.scr_y-2,0,ord('-'),self.scr_x)
                stdscr.refresh()
                self.content.append(line)
                line = ""
                self.draw_screen()
                self.stdscr.move(self.scr_y-1,0)
            elif ch == 27:
                self.mode = 1
            elif ch == curses.KEY_BACKSPACE:
                y,x = self.stdscr.getsyx()
                line = line[:-1]
                self.draw_inputArea(line)
                self.stdscr.move(y,x-1)
            else:
                if ch < 256:
                    string = chr(ch)
                else:
                    string = parse(ch)
                stdscr.addstr(string)
                line += string
        self._normal_loop()

    def _normal_loop(self):
        curses.cbreak()
        curses.noecho()
        pos_y,pos_x = self.stdscr.getsyx()
        move = self.stdscr.move
        while self.mode == 1:
            ch = stdscr.getch()
            if ch == curses.KEY_UP or ch == ord('k'):
                pos_y = self.check_pos('y',pos_y -= 1)
                move(pos_y, pos_x)
            elif ch == curses.KEY_DOWN or ch == ord('j'):
                pos_y = self.check_pos('y',pos_y += 1)
                move(pos_y, pos_x)
            elif ch == curses.KEY_LEFT or ch == ord('h'):
                pos_x = self.check_pos('x',pos_x -= 1)
                move(pos_y, pos_x)
            elif ch == curses.KEY_RIGHT or ch == ord('l'):
                pos_x = self.check_pos('x',pos_x += 1)
                move(pos_y, pos_x)
            elif ch == ord('i'):
                self.clear_input()
                self.mode = 0
        self._insert_loop()

if __name__ == "__main__":
    try:
        ui = UI()
        ui.start()
    finally:
        ui.end()
