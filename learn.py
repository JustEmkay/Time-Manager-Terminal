import curses
from curses import wrapper
from curses.textpad import Textbox,rectangle
from datetime import datetime , time as t
from models import Todo,today_stamp

x, y = 5, 5
menu_options : list[str] = ['Clock' ,'Task', 'Exit']

def menu(stdscr, options:list[str], indx:int , color) -> None:
    for idx,opt in enumerate(options):
        if idx == indx:
            stdscr.addstr(y+idx,x,opt,color)
        # elif idx+1 == len(options):
        #     stdscr.addstr(y+idx,x,"---------------")
        #     stdscr.addstr(y+idx+1,x,opt)
        else:
            stdscr.addstr(y+idx,x,opt)
    stdscr.addstr(y+idx+1,x,'-------------')
    stdscr.addstr(y+idx+2,x,f'selected: {options[indx]}')
    
def create_task(stdscr,color) -> None:
    stdscr.addstr(y,x,'What you want to accomplish?')
    win = curses.newwin(2,45,9,5)
    box = Textbox(win)
    rectangle(stdscr,x,y-1,15,50)
    stdscr.refresh()
    box.edit()
    stdscr.addstr(y+6,x,'Ctrl + G to exit edit')
    text = box.gather()
    stdscr.addstr(17,5,text)
    stdscr.getch()
    
    
    
def show_task(stdscr,color) -> None:
    tmenu_opt : list[str] = ['create','search','exit']
    tindex : int = 0
    while 1:
        stdscr.clear()
        menu(stdscr,tmenu_opt,tindex,color)
        stdscr.refresh()
        key = stdscr.getkey()

        if key == 'KEY_UP' and tindex > 0:
            tindex -= 1
        elif key == 'KEY_DOWN' and tindex < len(tmenu_opt)-1:
            tindex += 1
        elif key == 'KEY_ENTER' or key == '\n' or key == '\r':
            if tmenu_opt[tindex] == 'exit':
                return 0
            if tmenu_opt[tindex] == 'create':
                stdscr.clear()
                create_task(stdscr,color)
        
def show_clock(stdscr) -> None:
    stdscr.nodelay(True)
    stdscr.timeout(1000)
    # x : int = 2
    # y : int = 2
    
    while 1:
        clock = datetime.today().strftime("%B %d, %Y | %I:%M:%S %p")
        stdscr.clear()
        stdscr.addstr(x,y,clock,curses.A_BOLD)
        # time.sleep(1)
        stdscr.addstr(x+1,y,"press Q to exit")
        try:
            key = stdscr.getkey()
        except:
            key = None
        if key == "q" :
            stdscr.nodelay(False)        
            return 0


def main(stdscr) -> None:
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    RED_WHITE = curses.color_pair(1)
    GREEN_BLACK = curses.color_pair(2)
    
    menu_opt_indx : int = 0
    curses.curs_set(0)
    while 1:
        stdscr.clear()
        menu(stdscr,menu_options,menu_opt_indx,RED_WHITE)
        stdscr.refresh()
        key = stdscr.getkey()

        if key == 'KEY_UP' and menu_opt_indx > 0:
            menu_opt_indx -= 1
            
        elif key == 'KEY_DOWN' and menu_opt_indx < len(menu_options)-1:
            menu_opt_indx += 1
            
        elif key == 'KEY_ENTER' or key == '\n' or key == '\r':
            
            if menu_options[menu_opt_indx] == 'Exit':
                return 0
            elif menu_options[menu_opt_indx] == 'Clock':
                show_clock(stdscr)
            elif menu_options[menu_opt_indx] == 'Task':
                show_task(stdscr,GREEN_BLACK)

wrapper(main)