import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk


class offlinemode:
    def __init__(self,master):
        print("Offline_graph class called")

    def offline(self, master):

        self.master = master
        self.master.title("Pipeline Health Monitoring Robot: Online Mode")
        #create frame of the size of window
        self.x = self.master.winfo_screenwidth()
        self.y = self.master.winfo_screenheight()-90

        self.frame = tk.Frame(self.master, height= self.y, width=self.x, bg='light gray')
        self.frame.place(x=0,y=0)


        #for displaying data
        self.frame1 = tk.Frame(self.frame, height= self.y-50, width=self.x, bg='')
        self.frame1.place(x=0,y=0)
        
        #for control widgets
        self.frame2 = tk.Frame(self.frame, height= 50, width=self.x, bg='')
        self.frame2.place(x=0,y=self.y-100)

        
        self.fig = plt.figure()
        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(self.x/float(DPI),(self.y -100)/float(DPI))
        
        #make figure height according to window size
        
        t = np.arange(0.0,3.0,0.01)
        s = np.sin(np.pi*t)
        plt.plot(t,s)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame1)
        self.plot_widget = self.canvas.get_tk_widget()

        self.fig.canvas.draw()
        self.plot_widget.pack()

        self.quit_button = tk.Button(self.frame2, text="Quit", 
                                     bg="gray", bd=2, relief="raised",
                                     command=self.master.destroy)
        
        self.quit_button.place(x=self.x-200,y=10)


        self.back_button = tk.Button(self.frame2, text="Back", 
                                     bg="gray", bd=2, relief="raised",
                                     command= lambda: self.go_back_to_mode_selection())
        
        self.back_button.place(x=100,y=10)


    def go_back_to_mode_selection(self):
        
        #removing the current frame and passing thr empty root to new page
        #plt.close(self.fig)
        print("closed the figure")
        from mode_selection import mode_selection
        print("called mode selection class")
        self.frame.place_forget()
        self.frame1.place_forget()
        self.frame2.place_forget()
        
        

        mod = mode_selection(self.master)
        mod.mode(self.master)