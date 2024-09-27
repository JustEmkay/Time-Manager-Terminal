from datetime import datetime

today_stamp = int(datetime(datetime.now().year,datetime.now().month,datetime.now().day,0,0,0).timestamp())

class Todo:
    
    def __init__(self, task:str, priority : bool , urgent:bool,
                 status:bool = None ,task_date : int = None) -> None:
         
         self.task = task
         self.priority = priority
         self.urgent = urgent
         self.status = status if status is not None else False
         self.task_date = task_date if task_date is not None else int(today_stamp)
         
    def __str__(self) -> str:
          return f'{datetime.fromtimestamp(self.task_date).strftime("%d-%m-%Y")} : {self.task} | priority:{self.priority} | usrgent:{self.urgent} | status: {self.status}'
      

    def task_toDict(self) -> dict:
        
        result : dict = {
            'task' : self.task,
            'priority' : self.priority,
            'urgent' : self.urgent,
            'status' : self.status
        }
        
        return result 