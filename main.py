import json
import random
import time
from math import ceil
from curses import *


def start_screen(window, height, width, top, length):
    window.box()
    window.keypad(True)
    window.addstr(int(height/4)-top, int(width/4)-length, 'Start Game', A_REVERSE)
    window.addstr(int(height/4)-top, 3*int(width/4)-length, 'Quit')
    pos = "Start Game"
    while True:
        x = window.getkey()
        if x == 'KEY_RIGHT':
            pos = 'Quit'
            window.clear()
            window.box()
            window.addstr(int(height/4)-top, int(width/4)-length, 'Start Game')
            window.addstr(int(height/4)-top, 3*int(width/4)-length, 'Quit', A_REVERSE)
        if x == 'KEY_LEFT':
            pos = 'Start Game'
            window.clear()
            window.box()
            window.addstr(int(height/4)-top, int(width/4)-length, 'Start Game', A_REVERSE)
            window.addstr(int(height/4)-top, 3*int(width/4)-length, 'Quit')
        if x == '\n':
            if pos == 'Quit':
                return 'Q'
            elif pos == 'Start Game':
                return 'S'
            elif pos == 'Leaderboard':
                return 'L'
            elif pos == 'High Score':
                return 'H'


def update(window, height, width, num, score, country):
    window.clear()
    window.box()
    window.addstr(1, 1, ' '*(int(width/2) - 1) + '|', A_REVERSE)
    window.addstr(1, int(width/4), score, A_REVERSE)
    window.addstr(1, int(width/2), ' '*(int(width/2) - 1), A_REVERSE)
    window.addstr(1, 3*int(width/4), num, A_REVERSE)
    window.hline(int(height/2), 1, ord('-'), (width - 2))
    window.move(int(height/3), int(width/2) - int(len(country)/2))
    window.addstr(str(country))
    window.move(2*int(height/3), int(width/2) - 4)
    window.refresh()


def numupdate(window, height, width, num):
    window.clear()
    window.box()
    window.addstr(1, 1, ' '*(int(width/2) - 1) + '|', A_REVERSE)
    window.addstr(1, int(width/4), 'SCORE', A_REVERSE)
    window.addstr(1, int(width/2), ' '*(int(width/2) - 1), A_REVERSE)
    window.addstr(1, 3*int(width/4), 'TIME', A_REVERSE)
    window.hline(int(height/2), 1, ord('-'), (width - 2))
    window.move(int(height/3), int(width/2))
    window.addstr(str(num))
    window.move(2*int(height/3), int(width/2) - 4)
    window.refresh()



def main(stdscr):
    curs_set(0)
    height = 20
    width = 92
    top = 2
    length = 4
    win = newwin(height, width, top, length)
    while True:
        out = start_screen(win, height, width, top, length)
        if out == 'Q':
            return
        else:
            numupdate(win, height, width, 3)
            napms(1000)
            numupdate(win, height, width, 2)
            napms(1000)
            numupdate(win, height, width, 1)
            napms(1000)
            numupdate(win, height, width, 'GO!')
            start_time = time.time()
            score = 0
            elapsed_time = 0
            with open('config.json', 'r') as f:
                jstime = json.load(f)
            TIME = jstime["Time in Seconds"]
            with open('data.json', 'r') as f:
                js = json.load(f)
            cmd = ''
            country = random.choice(list(js.keys()))
            update(win, height, width, str(ceil(TIME - elapsed_time)), str(score), country)
            while elapsed_time < TIME:
                if cmd in js[country]:
                    country = random.choice(list(js.keys()))
                    cmd = ''
                    score += 1
                    update(win, height, width, str(ceil(TIME - elapsed_time)), str(score), country)
                x = win.getkey()
                try:
                    if len(x) == 1 and x != KEY_BACKSPACE and ord(x) != 8 and ord(x) != 127 and x != '\x7f' and ord(x) != 10 and ord(x) >= 32:
                        win.addch(x)
                        cmd += x
                    elif (ord(x) == 8 or ord(x) == 127 or ord(x) == KEY_BACKSPACE or x == '\x7f'):
                         if cmd != '':
                            cmd = cmd[0:-1]
                            win.addstr('\b \b')
                         else:
                            cmd = ''
                            win.move(2*int(height/3), int(width/2) - 4)
                    elif ord(x) == 10:
                        pass
                    elif ord(x) == 9 or ord(x) == 27:
                        country = random.choice(list(js.keys()))
                        update(win, height, width, str(ceil(TIME - elapsed_time)), str(score), country)
                        cmd = ''

                except:
                    pass
                elapsed_time =  time.time() - start_time
            win.clear()
            update(win, height, width, 'Press any key to continue', str(score), 'You scored ' + str(score) + '!')
            x = win.getkey()
            napms(2000)
            win.clear()


wrapper(main)
