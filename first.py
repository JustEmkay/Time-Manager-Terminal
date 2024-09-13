import curses,json,pytz
from curses import wrapper
from datetime import datetime , time as t
import time

file_path : str = "data\journal.json"
menu_items : list[str] = ['Home', 'Clock' ,'Reminder', 
                          'Journal', 'Exit']

today : int = datetime.combine(datetime.now(pytz.timezone('Asia/Calcutta')),t.min).timestamp()

def journal_data() -> dict:
    temp : dict = {
                'productivity' : 0,
                'mood' : 0,
                'agenda_not_done' : [],
                'agenda_done' : [],
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

    stdscr.clear()
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
                stdscr.addstr(counter,y,ix+" << EDIT",RED_WHITE) # display heading
                counter+=1 
            else:
                stdscr.addstr(counter,y,ix,curses.A_BOLD)
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
                stdscr.addstr(counter,y,item[ix])
        
            counter+=1                       
                                   
    # stdscr.refresh()
        
def journal(stdscr,RED_WHITE) -> None:
    
    j_index : int = -1
    stdscr.clear()  
    while 1:
        stdscr.addstr(x,y,f"Journal Date: {datetime.fromtimestamp(journal_today['created_date']).strftime('%B %d, %Y')}")
        stdscr.addstr(x+1,y,"__________________________________________")
        
        journal_menu(stdscr,j_index,RED_WHITE)
        stdscr.addstr(x+20,y,"Press q to exit journal")
        stdscr.addstr(x+21,y,"__________________________________________")
        # stdscr.addstr(x+6,y,str(j_index))
        
        key = stdscr.getkey()
        # stdscr.addstr(x+15,y,str(key))
                    
        if key == 'KEY_UP' and j_index > 0:
            j_index -= 1
        elif key == 'KEY_DOWN' and j_index < len(journal_options)-1:
            j_index += 1
        elif key == 'q':
            return 0

        stdscr.clear()
    stdscr.refresh()



def main(stdscr):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
    RED_WHITE = curses.color_pair(1)
    GREEN_WHITE = curses.color_pair(2)
    
    menu_selector_index : int = 0 
    # x , y = 5,5
    
    while 1:
        menu(stdscr,menu_items,menu_selector_index,x,y,RED_WHITE)
        stdscr.addstr(x+6,y,str(menu_selector_index))
        stdscr.addstr(x+6,y,f'Selected : {menu_items[menu_selector_index]}')

        key = stdscr.getkey()
        # stdscr.clear()
        stdscr.addstr(x+6,y,str(key))
        stdscr.refresh()
        # stdscr.getch()
                   
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
                
    # for i in range(1,10):
    #     stdscr.clear()
    #     stdscr.addstr(f'Saving data :  {i}% completed')
    #     time.sleep(1)    
    #     stdscr.refresh()


wrapper(main)
