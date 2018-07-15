import tkinter as tk
from PIL import Image, ImageTk
import sqlite3

class login:
    def __init__(self,master):
        print("Login class called")
        
    def frame_manager(self, master):   
        
        self.master = master
        self.master.title("Pipeline Health Monitoring Robot: Login")
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
        
        
        #add username, password fields
        self.cent_x = (self.x)/2
        self.cent_y = (self.y)/2
        
        self.frame_login = tk.Frame(bg_label, height= 200, width=500, bg="light gray", bd=2, relief="solid")
        self.frame_login.place(x = self.cent_x - 250, y=self.cent_y - 200)
        
        #self.username = StringVar()
        #self.passkey = StringVar()

        self.user_label = tk.Label(self.frame_login, text="Username",
                                   anchor="w", fg="black", bg="light gray")
        
        self.pass_label = tk.Label(self.frame_login, text="Password",
                                   anchor="w", fg="black", bg="light gray")
        
        self.user_entry = tk.Entry(self.frame_login, width = 25, bd=1, relief="solid")
        self.pass_entry = tk.Entry(self.frame_login, width = 25, bd=1, relief="solid", show="*")
        
        self.user_label.place(x=75,y=50)
        self.user_entry.place(x=200, y=50)
        
        self.pass_label.place(x=75, y=100)
        self.pass_entry.place(x=200, y=100)
        
        self.quit_button = tk.Button(self.frame_login, text="Quit", 
                                     bg="gray", bd=2, relief="raised",
                                     command=lambda: self.quitter())
        
        self.login_button = tk.Button(self.frame_login, text="Login",
                                      bg="gray", bd=2, relief="raised", 
                                      command=lambda: self.validator())
        
        self.quit_button.place(x=75,y=160)
        self.login_button.place(x=375, y=160)
        
        
        
        #add help, quit buttons
        
        
    def validator(self):
        
        user = self.user_entry.get()
        passkey = self.pass_entry.get()

        conn = sqlite3.connect('../databases/credential.db')
        c = conn.cursor()
        c.execute("SELECT * FROM userinfo")
        rows = c.fetchall()

        
        n = len(rows)
        
        counter = 0
        while(counter<= n):
            for j in rows:
                
                if(user in j and passkey in j):
                    
                    from mode_selection import mode_selection
                    #removing the current frame and passing thr empty root to new page
                    self.frame.pack_forget()
                    mod = mode_selection(self.master)
                    mod.mode(self.master)
                    
            break;    
            
        #create warning if no match is found
        
        self.warning_label = tk.Label(self.frame_login, text="Username or Passpword is incorrect.",
                                      bg="light gray", fg="red")
        self.warning_label.place(x=100, y = 125)


    def quitter(self):
        self.master.quit()