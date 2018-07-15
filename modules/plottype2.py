import tkinter as tk
import matplotlib
from matplotlib.widgets import Slider
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import numpy as np
from PIL import Image, ImageTk


class plottype2:
    def __init__(self,master):
        print("Offline_graph class called")

    def plot2(self, master, data):

        self.master = master
        self.data = data
        self.sensor_name = "LDR"
        self.master.title("Pipeline Health Monitoring Robot: Offline Mode: LED-LDR Sensor Data")
        #create frame of the size of window
        self.x = self.master.winfo_screenwidth()
        self.y = self.master.winfo_screenheight()-80

        self.frame = tk.Frame(self.master, height= self.y, width=self.x, bg='light gray')
        self.frame.place(x=0,y=0)

        
        #for displaying data
        self.frame1 = tk.Frame(self.frame, height= self.y-40, width=self.x, bg='')
        self.frame1.place(x=0,y=0)

        #for displaying toolbar
        self.frame0 = tk.Frame(self.frame, height = 40, width = self.x, bg='')
        self.frame0.place(x=10,y=10)
        
        #for control widgets
        self.frame2 = tk.Frame(self.frame, height= 40, width=self.x, bg='')
        self.frame2.place(x=0,y=self.y-40)

        
        #command for shared axis
        self.fig = plt.figure()
        

        #make figure height according to window size

        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(self.x/float(DPI),(self.y -40)/float(DPI))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame1)

        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack()
        self.fig.canvas.draw()
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame0)
        self.toolbar.update()
        self.canvas._tkcanvas.pack()

        t = np.arange(self.data.shape[0])
        y1 = self.data[:,4]
        y2 = self.data[:,5]
        y3 = self.data[:,6]
        y4 = self.data[:,7]

        self.encoder = self.data[:,8]

        encod = data[:,8]
        dist = (encod*np.pi*5)/(2400*100)
        custom_label = []
        for j in dist:
            j = round(j,2)
            custom_label.append(j)

        self.fig.suptitle("LED-LDR Sensor Data")

        self.ax1 = self.fig.add_subplot(4,1,1)
        self.ax1.plot(t,y1,'r',Linewidth=1.5,label="sensor1")
        #self.ax1.minorticks_on()
        #self.ax1.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        
        self.ax1.set_ylabel("Sensor1")

        self.ax2 = self.fig.add_subplot(4,1,2, sharex=self.ax1, sharey=self.ax1)
        self.ax2.plot(t,y2,'g',Linewidth=1.5,label="sensor2")
        #self.ax2.minorticks_on()
        #self.ax2.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        
        self.ax2.set_ylabel("Sensor2")

        self.ax3 = self.fig.add_subplot(4,1,3, sharex=self.ax1, sharey=self.ax1)
        self.ax3.plot(t,y3, 'violet', Linewidth=1.5,label="sensor3")
        #self.ax3.minorticks_on()
        #self.ax3.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        
        self.ax3.set_ylabel("Sensor3")

        self.ax4 = self.fig.add_subplot(4,1,4, sharex=self.ax1, sharey=self.ax1)
        self.ax4.plot(t,y4, 'orange', Linewidth=1.5,label="sensor4")
        #self.ax4.minorticks_on()
        self.ax4.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        #self.ax4.set_xticklabels(custom_label, rotation='vertical')
        self.ax4.set_ylabel("Sensor4")

        self.fig.subplots_adjust(hspace=0)
##########################################################################################

        self.view_size = 500
        self.total_size = t.shape[0] + 100

        self.ax1.set_xlim([0, self.view_size])
        #position of slider

        self.axpos = self.fig.add_axes([0.2, 0.01, 0.65, 0.03])
        self.spos = Slider(self.axpos, 'Position', 0, self.total_size - self.view_size, valinit=1, dragging=True)
        self.spos.on_changed(self.update)

############################################################################################

       
        self.fig.text(0.06, 0.5, 'Sensor Output', ha='center', va='center', rotation='vertical')
        #print("graph plotted")

        self.quit_button = tk.Button(self.frame2, text="Quit", 
                                     bg="gray", bd=2, relief="raised",
                                     command= lambda: self.quitter())
        
        self.quit_button.place(x=self.x-200,y=10)

        self.pvdf_button = tk.Button(self.frame2, text="PVDF Data", bg="gray", bd=2,relief="raised",
                                    command= lambda: self.pvdf_viewer())

        self.pvdf_button.place(x = self.x/4+20 , y=10)


        self.report_button = tk.Button(self.frame2, text="Show Report",
                                       bg="gray", bd=2, relief="raised",
                                       command= lambda: self.show_report())

        self.report_button.place(x = self.x /2+20 , y = 10)


        self.back_button = tk.Button(self.frame2, text="Back", 
                                     bg="gray", bd=2, relief="raised",
                                     command= lambda: self.go_back_to_file_selection())
        
        self.back_button.place(x=100,y=10)



    def update(self,val):
        pos = self.spos.val
        self.ax1.set_xlim([pos,pos+self.view_size])
        self.fig.canvas.draw_idle()

    def pvdf_viewer(self):
        self.frame.place_forget()
        from plottype3 import plottype3
        plot = plottype3(self.master)
        plot.plot3(self.master, self.data)

    def go_back_to_file_selection(self):
        
        #removing the current frame and passing thr empty root to new page
        #plt.close(self.fig)
        print("closed the figure")
        from fileselection import fileselection
        self.frame.place_forget()
        sel_file = fileselection(self.master)
        sel_file.file_selector(self.master)

    def show_report(self):

        print("report function called")

        from anomalies import anomalies
        self.frame.place_forget()
        report = anomalies(self.master)
        report.anomaly_table(self.master, self.sensor_name, self.data, self.encoder)   

    def quitter(self):
        plt.close(self.fig)
        self.master.quit()