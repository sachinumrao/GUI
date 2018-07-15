import tkinter as tk
from login import login

class window_manager:
    def __init__(self, master):
        self.master = master
        self.master.title("Pipeline Health Monitoring Robot: Data Analyser")
        
        log = login(self.master)#create object of login class
        log.frame_manager(self.master)    
         
    
if __name__ == '__main__':
    
    root = tk.Tk()
    #root.state('-zoomed')
    root.state('zoomed')
    #root.attributes("-topmost", True)
    gui = window_manager(root)
    root.mainloop()
    