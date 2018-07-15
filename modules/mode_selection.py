import tkinter as tk
from PIL import Image, ImageTk

class mode_selection:
    def __init__(self,master):
        print("Mode Selection class called")
        
    def mode(self, master): 
                
        self.master = master
        self.master.title("Pipeline Health Monitoring Robot: Mode Selection")
        #create frame of the size of window
        self.x = self.master.winfo_screenwidth()
        self.y = self.master.winfo_screenheight()-80
        self.frame = tk.Frame(self.master, height= self.y, width=self.x)
        self.frame.pack()
        
        #add background image
        
        image1 = Image.open("../images/background.png")
        new_image1 = image1.resize((self.x,self.y),Image.ANTIALIAS)
        photo1 = ImageTk.PhotoImage(new_image1)
        bg_label = tk.Label(image=photo1)
        bg_label.image=photo1
        bg_label.place(x=0, y=0)
        
        #add offline and online mode buttons
        self.cent_x = (self.x)/2
        self.cent_y = (self.y)/2
        
        self.frame_mode = tk.Frame(bg_label, height= 200, width=500, bg="light gray", bd=2, relief="solid")
        self.frame_mode.place(x = self.cent_x - 250, y=self.cent_y - 200)
        
        
        self.online_button = tk.Button(self.frame_mode, text="Online Mode",
                                       bg="gray", bd=2, relief="raised",
                                       command = lambda: self.online_mode())
        
        self.offline_button = tk.Button(self.frame_mode, text="Offline Mode",
                                        bg="gray", bd=2, relief="raised",
                                        command = lambda: self.offline_mode())
        
        self.back = tk.Button(self.frame_mode, text="Back", 
                              bg="gray", bd=2, relief="raised", 
                              command = lambda: self.go_back_to_login())

        self.quit = tk.Button(self.frame_mode, text="Quit", 
                              bg="gray", bd=2, relief="raised", 
                              command = lambda: self.quitter())
        
        self.online_button.place(x=200, y=30)
        self.offline_button.place(x=200, y=80)
        self.back.place(x=75, y=160)
        self.quit.place(x=375, y=160)
        
    def online_mode(self):
        print("online mode called")
        
        from online_graph import online_graph
        self.frame.pack_forget()
        mode = online_graph()
        
        
        
        
    def offline_mode(self):
        print("offline mode called")
        from fileselection import fileselection
        self.frame.pack_forget()
        sel_file = fileselection(self.master)
        sel_file.file_selector(self.master)


    def go_back_to_login(self):

        from login import login
        log = login(self.master)
        log.frame_manager(self.master) 
        
    def quitter(self):
        self.master.destroy()