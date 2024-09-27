import curses
from curses import wrapper
from curses.textpad import Textbox,rectangle
from datetime import datetime , time as t
from models import Todo,today_stamp
import time

x, y = 5, 5
menu_options : list[str] = ['clock' ,'task', 'exit']


tasks_data : dict = { 
    1727308800 : [
        {
            'task' : 'learn windows and pads',
            'priority': True,
            'urgent' : False,
            'status' : False
        },
        {
            'task' : "Do 50 percentage of import option",
            'priority': True,
            'urgent' : False,
            'status' : False
        },
        {
            'task' : "Fix resume",
            'priority': False,
            'urgent' : True,
            'status' : False
        },
    ],
    today_stamp : [ ]
}

def percentage():
    win = curses.newwin(3, 32, 1, 4)
    win.border(0)
    loading = 0
    while loading < 100:
        loading += 1
        time.sleep(0.03)
        update_progress(win, loading)

def update_progress(win, progress):
    rangex = (30 / float(100)) * progress
    pos = int(rangex)
    display = '#'
    if pos != 0:
        win.addstr(1, 1, "{}".format(display*pos))
        win.addstr(1, 10, "loading")
        win.refresh()

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

def insert_task(task) -> dict:
    try: 
        if today_stamp in tasks_data:
            tasks_data[today_stamp].append(task)
            return {
                'status' : True,
                'error' : False,
                'message' : "Added as today's task" 
            }
            
        else:
            tasks_data.update(
                {
                    today_stamp : task
                    
                }
            )
            
            return {
                'status' : True,
                'error' : False,
                'message' : "Created today and added as task." 
            }
            
        
    except Exception as e:
        return {
                'status' : False,
                'error' : True,
                'message' : e 
            }
         
def create_task(stdscr,color) -> None:
    # win = curses.newwin(2,45,4,6) # nlines: int, ncols: int, begin_y: int, begin_x: int
    # box = Textbox(win)
    # rectangle(stdscr,3,5,6,51)  # win: _CursesWindow, uly: int, ulx: int, lry: int, lrx: int
    # stdscr.refresh()
    # box.edit()
    
    curses.curs_set(1)
    
    stdscr.addstr(5,5,'What you want to accomplish?',curses.A_BOLD)
    stdscr.addstr(6,5,'Ctrl + G to exit edit')
    win = curses.newwin(1,50,7,5)
    box = Textbox(win)
    stdscr.refresh()
    box.edit()
    task_input = box.gather()
    stdscr.addstr(9,5,f'Task:',curses.A_BOLD)
    stdscr.addstr(9,11,task_input,color)
    
    while 1:
        curses.curs_set(1)
        
        stdscr.addstr(11,5,"Press : 'Y' to Continue / 'N' to Cancel")
        key = stdscr.getkey()
        stdscr.addstr(12,5,key)
        time.sleep(0.2)
        
        if key == 'y' or key == 'Y':
            curses.curs_set(0)
            
            stdscr.clear()
            stdscr.addstr(5,5,f'Task:',curses.A_BOLD)
            stdscr.addstr(5,11,task_input,color | curses.A_BOLD)
            stdscr.addstr(6,5,'Priority of the task:',curses.A_BOLD)
            stdscr.addstr(8,5," Press: 'Y' important / 'N' Not-important")
            while 1:
                key = stdscr.getkey()

                if key == 'y' or key == 'Y':
                    priority : bool = True
                    break
                elif key == 'n' or key == 'N':
                    priority : bool = False
                    break
                
            stdscr.clear()
            stdscr.addstr(5,5,f'Task:',curses.A_BOLD)
            stdscr.addstr(5,11,task_input,color | curses.A_BOLD)
            stdscr.addstr(6,5,'Urgency of the task:',curses.A_BOLD)
            stdscr.addstr(8,5," Press: 'Y' Urgent / 'N' Not-urgent")
            while 1: 
                key = stdscr.getkey()
                    
                if key == 'y' or key == 'Y':
                    urgent : bool = True
                    break
                elif key == 'n' or key == 'N':
                    urgent : bool = False
                    break
                
            t = Todo(task_input,priority,urgent)
            
            stdscr.clear()
            stdscr.addstr(5,5,str(t),curses.A_BOLD | curses.COLOR_GREEN)
            stdscr.getch()
            
            insert_task(t.task_toDict())
            percentage()
            
            return 0
            
        
        elif key == 'n' or key == 'N':
            return 0

def today_task(stdscr,color) -> None:
    stdscr.clear()
    task_slct_index : int = 1
    while 1:
        stdscr.addstr(5,5,f"Today: {datetime.fromtimestamp(today_stamp).strftime('%d %A %B %Y')}",
                    curses.A_UNDERLINE | curses.A_BOLD)
        stdscr.addstr(6,5,'Press q to exit')
        if today_stamp in tasks_data:
            for idx,task in enumerate(tasks_data[today_stamp],start=1):
                if task_slct_index == idx:
                    stdscr.addstr(8+idx,5,task['task'], curses.COLOR_RED | curses.A_BOLD)
                else:
                    stdscr.addstr(8+idx,5,task['task'],curses.A_BOLD)
                    
            if len(tasks_data[today_stamp]) < 1:
                stdscr.addstr(8, 5,"No task found.",curses.A_ITALIC)  
        else:                   
            stdscr.addstr(8, 5,"No task found.",curses.A_ITALIC)  
                    
        stdscr.refresh()

        key = stdscr.getkey()

        if key == 'KEY_UP' and task_slct_index > 1:
            task_slct_index -= 1
        elif key == 'KEY_DOWN' and task_slct_index < len(tasks_data[today_stamp]):
            task_slct_index += 1
        
        elif key == 'KEY_ENTER' or key == '\n' or key == '\r':
            pass
        
        elif key == "q":
            stdscr.nodelay(False)
            return 0



                    
    

         
def show_task(stdscr,color) -> None:
    stdscr.nodelay(False)
    tmenu_opt : list[str] = ['create','today','search','exit']
    tindex : int = 0
    while 1:
        stdscr.clear()
        menu(stdscr,tmenu_opt,tindex,color)
        stdscr.refresh()
        try:
            key = stdscr.getkey()
        except:
            key = None

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
            if tmenu_opt[tindex] == 'today':
                today_task(stdscr,color)
        
def show_clock(stdscr) -> None:
    stdscr.nodelay(True)
    stdscr.timeout(1000)
    
    clock_win = curses.newwin(3, 40, 2, 5)
    if today_stamp not in tasks_data:
        tasks_win = curses.newwin( 5, 65, 6, 5)
    else:
        tasks_win = curses.newwin(len(tasks_data[today_stamp]) + 2, 65, 6, 5)
    
    while True:
        clock = datetime.today().strftime("%B %d, %Y | %I:%M:%S %p")

        clock_win.clear()
        clock_win.addstr(0, 0, clock, curses.A_BOLD)
        clock_win.addstr(1, 0, "Press 'q' to exit")
        clock_win.refresh()

        tasks_win.clear()
        tasks_win.addstr(0, 0, "Tasks for Today:", curses.A_UNDERLINE)
        
        if today_stamp in tasks_data:
            for idx, task in enumerate(tasks_data[today_stamp], start=1):
                task_str = f"{idx}. {task['task']} [Priority: {'Yes' if task['priority'] else 'No'}, Urgent: {'Yes' if task['urgent'] else 'No'}]"
                if not task['status']:
                    tasks_win.addstr(idx, 0, task_str,curses.A_BOLD)
                else:
                    tasks_win.addstr(idx, 0, f'{task_str}')
                    
            if len(tasks_data[today_stamp]) < 1:
                tasks_win.addstr(1, 0,"No task found.")    
        else:
            tasks_win.addstr(1, 0,"No task found.")

        tasks_win.refresh()

        try:
            key = stdscr.getkey()
        except:
            key = None
        if key == "q":
            stdscr.nodelay(False)
            stdscr.timeout(0)
            return 0



def main(stdscr) -> None:
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    RED_WHITE = curses.color_pair(1)
    GREEN_BLACK = curses.color_pair(2)
    
    menu_opt_indx : int = 0
    curses.curs_set(0)
    while 1:
        
        stdscr.clear()
        menu(stdscr,menu_options,menu_opt_indx,RED_WHITE)
        stdscr.refresh()
        
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key == 'KEY_UP' and menu_opt_indx > 0:
            menu_opt_indx -= 1
            
        elif key == 'KEY_DOWN' and menu_opt_indx < len(menu_options)-1:
            menu_opt_indx += 1
            
        elif key == 'KEY_ENTER' or key == '\n' or key == '\r':
            
            if menu_options[menu_opt_indx] == 'exit':
                return 0
            elif menu_options[menu_opt_indx] == 'clock':
                stdscr.clear()
                show_clock(stdscr)
            elif menu_options[menu_opt_indx] == 'task':
                show_task(stdscr,GREEN_BLACK)

wrapper(main)