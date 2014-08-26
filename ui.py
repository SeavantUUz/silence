#coding: utf-8
import curses
from tools import *
import sys,traceback

class UI(object):
    def __init__(self,sock=None):
        self.content = []
        self.mode = 0
        self.is_started = False
        self.sock = sock

    def append(self, line):
        self.content.append(line)

    def start(self):
        self.stdscr = curses.initscr()
        draw_line(self.stdscr,y-2,x)
        self.is_started = True

    def run(self):
        try:
            if not self.is_started:
                self.start()
            self._insert_loop()
        except:
            traceback.print_ex(file=sys.stdout)
        finally:
            self.end()

    def end(self):
        curses.endwin()

    def _insert_loop(self):
        curses.noecho()
        curses.cbreak()
        line = ''
        src_y, src_x = self.stdscr.getmaxyx()
        move(src_y-1,src_x)
        while self.mode == 0:
            ch = self.stdscr.getch()
            src_y, src_x = self.stdscr.getmaxyx()
            if ch == 10:
                self.stdscr.clear()
                self.stdscr.refresh()
                self.content.append(line)
                line = ''
                draw_screen(self.stdscr, self.content,srx_y-3,srx_x-1)
                draw_line(self.stdscr,src_y-2,0)
                if self.sock:
                    self.sock.send(line)
            elif ch == 27:
                self.mode = 1
                line = ''
                move(self.stdscr,src_y-1,0)
                self.stdscr.clrtoeol()
                self.stdscr.refresh()
            elif ch == 127:
                y,x = curses.getsyx()
                line = line[:-1]
                draw_input(self.stdscr, line, y, x-1)
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
            pos_y,pos_x = curses.getsys()
            while self.mode == 1:
                ch = self.stdscr.getch()
                if ch == curses.KEY_UP or ch == ord('k'):
                    pos_y = check_pos('y',pos_y-1)
                    move(pos_y,pos_x)
                elif ch == curses.KEY_DOWN or ch == ord('j'):
                    pos_y = check_pos('y',pos_y+1)
                    move(pos_y,pos_x)
                elif ch == curses.KEY_LEFT or ch == ord('h'):
                    pos_x = check_pos('x',pos_x-1)
                    move(pos_y,pos_x)
                elif ch == curses.KEY_RIGHT or ch == ord('l'):
                    pos_x = check_pos('x',pos_x+1)
                    move(pos_y,pos_x)
                elif ch == ord('i'):
                    self.mode = 0
            self._insert_loop()

        
