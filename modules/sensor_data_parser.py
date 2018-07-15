import pandas as pd
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from collections import Counter

class sensor_data_parser:

    def __init__(self, master):
        print("sensor data parser is called")

    def parser_func(self, master, filename):
        self.fname = filename
        self.master = master
        self.master.title("Pipeline Health Monitoring Robot: Processing Sensor Data")
        #create frame of the size of window
        self.x = self.master.winfo_screenwidth()
        self.y = self.master.winfo_screenheight()-80
        self.frame = tk.Frame(self.master, height= self.y, width=self.x)
        self.frame.pack()
        
        print(self.fname)
        #add background image
        
        image1 = Image.open("../images/background.png")
        new_image1 = image1.resize((self.x,self.y),Image.ANTIALIAS)
        photo1 = ImageTk.PhotoImage(new_image1)
        bg_label = tk.Label(image=photo1)
        bg_label.image=photo1
        bg_label.place(x=0, y=0)

        #file reading and data processing
        #Extact data of the required run from the full datalog

        input_file_name = self.fname
        tmp_file_name = '../tmp/data_new.txt'

        tmp_file = open(tmp_file_name,'w')
        input_file = open(input_file_name,'r+')

        
        for line in input_file:
            if (line[0]=='-' or line[0]=='M'):
                continue
            else:
                tmp_file.write(line)

        
        tmp_file.close()
        input_file.close()

        #read extracted data
        
        data = np.loadtxt(tmp_file_name, delimiter=',')
        #data = np.array(data)

        dim = data.shape[1]
        print("No. of channels: ",data.shape[1])
        

        #check if given file is from front or back module
        if(dim==9):
            self.graph_type=0
        if(dim==5):
            self.graph_type=1

        
        self.load_graph(data)
        

        

    def load_graph(self,data):
        if(self.graph_type==1):
            print("MFL data is provided, call graph type 1")
            self.frame.pack_forget()
            from plottype1 import plottype1
            plot = plottype1(self.master)
            plot.plot1(self.master, data)

        else:
            print("LDR + PVDF data is provided, call graph_type2")
                        
            self.frame.pack_forget()
            from plottype2 import plottype2
            plot = plottype2(self.master)
            plot.plot2(self.master, data)

    