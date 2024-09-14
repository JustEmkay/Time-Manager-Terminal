import curses,json,pytz
from curses import wrapper
from curses.textpad import Textbox,rectangle
from datetime import datetime , time as t
import time

file_path : str = r"data/journal.json"
menu_items : list[str] = ['Home', 'Clock' ,'Reminder', 
                          'Journal', 'Exit']

today : int = datetime.combine(datetime.now(pytz.timezone('Asia/Calcutta')),t.min).timestamp()

def journal_data() -> dict:
    temp : dict = {
                'productivity' : 0,
                'mood' : 0,
                'agenda_not_done' : ['Go for walk'],
                'agenda_done' : ['do home work'],
                'thankful' : ['im still alive', 'no need to use rope'],
                'lessons' : "",
                'sucks' : 'sleep early/ wake up at 5am',
                'created_date' : today
                        }
    
    try:
        with open(file_path) as fp:
                journal_stored_data = json.load(fp)
                if not journal_stored_data:
                    return temp
                if journal_stored_data[-1]['created_date'] == today:
                    return journal_stored_data[-1]
                else:
                    return temp
    except Exception as e:
        print(f'Error in journal_data.func : {e} ')
        return temp

journal_today = journal_data() # journal_data return dict from json file

journal_options : list = [
    { #0
        "Today's agenda" : [
        journal_today['agenda_not_done'],
        journal_today['agenda_done']
        ]
    },
    { #1
        "Today, I am Thankful for..." : journal_today['thankful']
    },
    { #2
        "Today's Lesson" : journal_today['lessons']
    },
    { #3
        "One thing I did that su*ked" : journal_today['sucks']
    }
    ]

x : int = 5
y : int = 5

def menu(stdscr,options,ms_index,x,y,RED_WHITE) -> None:

    # stdscr.clear()
    
    stdscr.addstr(x-2,y,'Raspi-Terminal-app',curses.COLOR_GREEN)    
    for idx,items in enumerate(options):
        if idx == ms_index:
            stdscr.addstr(idx+x,y,items,RED_WHITE)    
        else:
            stdscr.addstr(idx+x,y,items)
        stdscr.refresh()
               
def clock(stdscr,RED_WHITE) -> None:
    stdscr.nodelay(True)
    
    # x : int = 2
    # y : int = 2
    
    while 1:
        clock = datetime.today().strftime("%B %d, %Y | %I:%M:%S %p")
        stdscr.clear()
        stdscr.addstr(x,y,clock,curses.A_BOLD)
        time.sleep(1)
        stdscr.addstr(x+1,y,"press Q to exit")
        try:
            key = stdscr.getkey()
        except:
            key = None
        if key == "q" :
            stdscr.nodelay(False)        
            return 0
        stdscr.refresh()

def journal_menu(stdscr,j_index,RED_WHITE)->None:
    stdscr.refresh()
    counter=8
    for idx,item in enumerate(journal_options): # idx-> index| item->{}
        for ix in item: # ix-> key of item dict
            if idx == j_index:
                stdscr.addstr(counter,y,ix+" << EDIT",RED_WHITE | curses.A_STANDOUT) # display heading
                counter+=1 
            else:
                stdscr.addstr(counter,y,ix,curses.A_BOLD | curses.A_UNDERLINE)
                counter+=1
                
            if idx == 0:
                for indx_a,agnda in enumerate(item[ix]):
                    if indx_a == 0 and agnda:
                        for ag in agnda:
                            stdscr.addstr(counter,y,'[ ]'+ag)
                            counter+=1
                    elif indx_a == 1 and agnda:
                        for ag in agnda:
                            stdscr.addstr(counter,y,'[X]'+ag)
                            counter+=1
                    else:
                        stdscr.addstr(counter,y,'Empty')
                        counter+=1
                                    
            elif idx == 1:
                for indx_t, thk in enumerate(item[ix]):
                    if thk:
                        stdscr.addstr(counter,y,str(indx_t+1)+'.'+thk)
                        counter+=1
                    else:
                        stdscr.addstr(counter,y,'Empty')
                        counter+=1
                        
            else:
                if item[ix] == "":
                    stdscr.addstr(counter,y,'Null')
                else:
                    stdscr.addstr(counter,y,item[ix])
                counter+=1
                
        
            counter+=1                       
                                   
    # stdscr.refresh()

def journal_edit(stdscr,edit_opt) -> None:
    stdscr.clear()
    if edit_opt == 'edit_agenda':
        # stdscr.addstr(x+1,y,"Edit: Today's Agends") #6 5 
        # stdscr.addstr(x+2,y,"_____________________________________________") #7 5
        
        # win = curses.newwin(1,45,9,5)
        # box = Textbox(win)
        # rectangle(stdscr,x,y-1,15,50)
        
        # stdscr.refresh()
        # box.edit()
        # text = box.gather()
        # stdscr.addstr(17,5,text)
        
        # stdscr.getch()
        pass
        
    elif edit_opt == 'edit_thank':
        pass
    elif edit_opt == 'edit_lessons':
        pass
    elif edit_opt == 'edit_sucks':
        pass
    stdscr.refresh()
            
def journal(stdscr,RED_WHITE) -> None:
    
    j_index : int = -1
    stdscr.clear()  
    while 1:
        stdscr.addstr(x,y,f"Journal Date: {datetime.fromtimestamp(journal_today['created_date']).strftime('%B %d, %Y')}")
        stdscr.addstr(x+1,y,"__________________________________________")
        
        journal_menu(stdscr,j_index,RED_WHITE)
        
        stdscr.addstr(x+18,y,"Press Up/Down to select")
        stdscr.addstr(x+19,y,"Press Enter to Edit")
        stdscr.addstr(x+20,y,"Press q to exit journal")
        stdscr.addstr(x+21,y,"__________________________________________")
        
        key = stdscr.getkey()
          
        if key == 'KEY_UP' and j_index > 0:
            j_index -= 1
        elif key == 'KEY_DOWN' and j_index < len(journal_options)-1:
            j_index += 1
        elif key == 'q':
            return 0
        elif key == 'KEY_ENTER' or key == '\n' or key == '\r':
            if j_index == 0:
                journal_edit(stdscr,'edit_agenda')
            elif j_index == 1:
                journal_edit(stdscr,'edit_thank')
            elif j_index == 2:
                journal_edit(stdscr,'edit_lessons')
            elif j_index == 3:
                journal_edit(stdscr,'edit_sucks')
                    
        

        stdscr.clear()
    stdscr.refresh()


def main(stdscr):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    RED_WHITE = curses.color_pair(1)
    GREEN_BLACK = curses.color_pair(2)
    
    menu_selector_index : int = 0 
    # x , y = 5,5
    
    while 1:
        stdscr.clear()
        menu(stdscr,menu_items,menu_selector_index,x,y,RED_WHITE)
        stdscr.addstr(x+6,y,str(menu_selector_index))
        stdscr.addstr(x+6,y,f'Selected : {menu_items[menu_selector_index]}')

        key = stdscr.getkey()
        stdscr.addstr(x+6,y,str(key))
        stdscr.refresh()

        if key == 'KEY_UP' and menu_selector_index > 0:
            menu_selector_index -= 1
        elif key == 'KEY_DOWN' and menu_selector_index < len(menu_items)-1:
            menu_selector_index += 1
        elif key == 'KEY_ENTER' or key == '\n' or key == '\r':
   
            if menu_items[menu_selector_index] == 'Clock':
                clock(stdscr,RED_WHITE)
            elif menu_items[menu_selector_index] == 'Journal':
                journal(stdscr,RED_WHITE)
            elif menu_items[menu_selector_index] == 'Exit':
                return 0
                



wrapper(main)
