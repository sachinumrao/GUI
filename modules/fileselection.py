import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

class fileselection:
    def __init__(self,master):
        print("File selection class called")

    def file_selector(self, master):
        self.master = master
        self.master.title("Pipeline Health Monitoring Robot: Select Sensor Datalog")
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

        #frame for file selection

        self.cent_x = (self.x)/2
        self.cent_y = (self.y)/2
        
        self.frame_file = tk.Frame(bg_label, height= 200, width=500, bg="light gray", bd=2, relief="solid")
        self.frame_file.place(x = self.cent_x - 250, y=self.cent_y - 200)
        
        
        self.label1 = tk.Label(self.frame_file, text="Datalog", anchor="w", fg="black", bg="light gray")


        self.file_entry = tk.Entry(self.frame_file, width = 25, bd=1, relief="solid")


        self.file_entry.bind("<1>",self.file_opener)
        self.filename = ''

        self.analyze = tk.Button(self.frame_file, text="Analyze", 
                                       bg="gray", command = lambda: self.analyze_data())
        
        self.back = tk.Button(self.frame_file, text="Back",
                                        bg="gray", command = lambda: self.go_back_to_mode_selection())

        self.quit = tk.Button(self.frame_file, text="Quit",
                                        bg="gray", command = lambda: self.quitter())
        
        
        self.label1.place(x=50, y=80)
        self.file_entry.place(x=120, y=80)
        self.analyze.place(x = 375 , y = 75)
        self.back.place(x = 75, y = 160)
        self.quit.place(x = 375, y = 160)
        

    def file_opener(self, event):

        print("file dialog opener called")
        self.filename = askopenfilename()
        s1 = self.filename
        s2 = s1.split('/')[-1]
        self.file_entry.insert(0, s2)

    def go_back_to_mode_selection(self):

        from mode_selection import mode_selection
        print("called mode selection class")
        self.frame.place_forget()  
        mod = mode_selection(self.master)
        mod.mode(self.master)


    def analyze_data(self):

        from sensor_data_parser import sensor_data_parser
        self.frame_file.place_forget()
        data_parser = sensor_data_parser(self.master)
        data_parser.parser_func(self.master,self.filename)

    def quitter(self):
        self.master.quit()
