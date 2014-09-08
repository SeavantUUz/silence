#coding: utf-8
import curses
from tools import *
import sys,traceback
import logging
import socket

class UI(object):
    def __init__(self,sock=None):
        self.content = []
        self.mode = 0
        self.is_started = False
        self.sock = sock
        self.is_continue = True
        self.is_update = False
        self.interrupt_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def append(self, line):
        logging.info(line)
        self.is_update = True
        self.content.append(line)

    def start(self):
        self.interrupt_sock.connect('interrupt.sock')
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)
        y,x = self.stdscr.getmaxyx()
        draw_line(self.stdscr,y-2,x)
        self.is_started = True

    def run(self):
        try:
            if not self.is_started:
                self.start()
            self._insert_loop()
        except:
            logging.info("error")
        finally:
            self.end()

    def end(self):
        self.is_continue = False
        logging.info("curses end")
        curses.endwin()

    def _insert_loop(self):
        curses.noecho()
        curses.cbreak()
        line = ''
        src_y, src_x = self.stdscr.getmaxyx()
        move(self.stdscr,src_y-1,0)
        try:
            while self.mode == 0:
                ch = self.stdscr.getch()
                src_y, src_x = self.stdscr.getmaxyx()
                if self.is_update:
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    draw_screen(self.stdscr, self.content,src_y-3,src_x-1)
                    draw_line(self.stdscr,src_y-2,src_x)
                    draw_input(self.stdscr, line, src_y-1, len(line))
                    self.is_update = False
                if ch == -1:
                    continue
                elif ch == 10:
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    self.content.append(line)
                    line = ''
                    draw_screen(self.stdscr, self.content,src_y-3,src_x-1)
                    draw_line(self.stdscr,src_y-2,src_x)
                    move(self.stdscr,src_y-1,0)
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
        except:
            self._insert_loop()
        self._normal_loop()

    def _normal_loop(self):
        curses.cbreak()
        curses.noecho()
        pos_y,pos_x = curses.getsyx()
        try:
            while self.mode == 1:
                ch = self.stdscr.getch()
                src_y, src_x = self.stdscr.getmaxyx()
                if self.is_update:
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    draw_screen(self.stdscr, self.content,src_y-3,src_x-1)
                    draw_line(self.stdscr,src_y-2,src_x)
                    draw_input(self.stdscr, line, src_y-1, len(line))
                    self.is_update = False
                if ch == -1:
                    continue
                elif ch == curses.KEY_UP or ch == ord('k'):
                    pos_y = check_pos(self.stdscr,'y',pos_y-1)
                    move(self.stdscr,pos_y,pos_x)
                elif ch == curses.KEY_DOWN or ch == ord('j'):
                    pos_y = check_pos(self.stdscr,'y',pos_y+1)
                    move(self.stdscr,pos_y,pos_x)
                elif ch == curses.KEY_LEFT or ch == ord('h'):
                    pos_x = check_pos(self.stdscr,'x',pos_x-1)
                    move(self.stdscr,pos_y,pos_x)
                elif ch == curses.KEY_RIGHT or ch == ord('l'):
                    pos_x = check_pos(self.stdscr,'x',pos_x+1)
                    move(self.stdscr,pos_y,pos_x)
                elif ch == ord('q'):
                    self.interrupt_sock.send("end")
                    break
                elif ch == ord('i'):
                    self.mode = 0
        except:
            self._normal_loop()
        self._insert_loop()
        
