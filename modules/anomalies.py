import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk

class anomalies:

    def __init__(self, master):
        print("anomalies class is called.")

    def anomaly_table(self,master,sensor_name, data, encoder):
        self.master = master
        self.data = data
        self.encoder = encoder
        self.sensor_name = sensor_name
        self.master.title("Pipeline Health Monitoring Robot: "+self.sensor_name+" Sensor Data Anomaly Report")
        #create frame of the size of window
        self.x = self.master.winfo_screenwidth()
        self.y = self.master.winfo_screenheight()-80
        self.frame = tk.Frame(self.master, height= self.y, width=self.x, bg="light gray")
        self.frame.place(x=0,y=0)
        
        #add background image
        
        image1 = Image.open("../images/background.png")
        new_image1 = image1.resize((self.x,self.y-40),Image.ANTIALIAS)
        photo1 = ImageTk.PhotoImage(new_image1)
        bg_label = tk.Label(image=photo1)
        bg_label.image=photo1
        bg_label.place(x=0, y=0)
        
        #frame0 on top of background image

        #parse data for anomaly

        #top frame for entry widget to input threhold level

        self.frame1 = tk.Frame(bg_label, height=40, width= self.x-20, bg="light gray")
        self.frame1.place(x=10,y=10)

        self.thresh_label = tk.Label(self.frame1, text="Threshold Value (0-1023)", anchor="w", fg="black", bg="light gray")

        self.thresh_entry = tk.Entry(self.frame1, width = 25, bd=1, relief="solid")

        self.report_button = tk.Button(self.frame1, text="Show Report", bg="gray", bd=2, relief="raised", 
                                       command=lambda: self.show_report())

        self.thresh_label.place(x = 50, y =10)
        self.thresh_entry.place(x = self.x/2 - 100 , y = 10)
        self.report_button.place(x = self.x - 200 , y =10)


        #frame for the anomaly table
        
        self.frame2 = tk.Frame(bg_label, height=self.y-124, width= self.x-40, bg="light gray")
        self.frame2.place(x=20,y=60)
        

        #frame for the control at the bottom of the page
        self.frame3 = tk.Frame(self.frame, height=40, width = self.x-20, bg="light gray")
        self.frame3.place(x=10,y=self.y - 40)

        self.back_button = tk.Button(self.frame3, text="Back", bg="gray", bd=2, relief="raised", 
                                     command= lambda: self.go_to_plot())

        self.quit = tk.Button(self.frame3, text="Quit", bg="gray", bd=2, relief="raised", 
                              command= lambda: self.quitter())

        self.back_button.place(x= 100, y =10)
        self.quit.place(x = self.x-200, y =10)



    def quitter(self):
        self.master.quit()


    def go_to_plot(self):
        print("going back to plot of"+ self.sensor_name)
        if(self.sensor_name=="MFL"):
            print("go back to plot of MFL sensor")
            from plottype1 import plottype1
            self.frame.place_forget()
            plot = plottype1(self.master)
            plot.plot1(self.master, self.data)

        if(self.sensor_name=="LDR"):
            print("go back to plot of LDR sensor")
            from plottype2 import plottype2
            self.frame.place_forget()
            plot = plottype2(self.master)
            plot.plot2(self.master, self.data)

        if(self.sensor_name=="PVDF"):
            print("go back to plot of PVDF sensor")
            from plottype3 import plottype3
            self.frame.place_forget()
            plot = plottype3(self.master)
            plot.plot3(self.master, self.data)


    def show_report(self):
        print("displaying report")

        

        if(self.sensor_name == "MFL"):
            data = self.data[:,0:4]

        elif(self.sensor_name == "PVDF"):
            data = self.data[:,0:4]
        else:
            data = self.data[:,4:8]

        encoder = self.encoder

        print("Data recieved successfully")    

        thres = self.thresh_entry.get()

        #find thre sub portions in values above threshold
        s_max = 1023
        x = thres = 600
        delta = (s_max - x)//3

        low = thres + delta
        high = s_max - delta

        #emmmpty list to get values in proper structure
        # [sensor_id, values_index, sensor_value, encoder_value]


        HIGH = [[]]
        LOW = [[]]
        MED = [[]]

        #filter data into three lists
        for i in range(data.shape[0]):
            for j in range(4):
                alert = None
                if(thres<data[i,j] and data[i,j]<= low):
                    alert = "low"
                    LOW.append([j , i , data[i,j], encoder[i]])
                    
                elif(high<data[i,j] and data[i,j]<=s_max):
                    alert = "high"
                    HIGH.append([j , i , data[i,j], encoder[i]])
                    
                elif(low<data[i,j] and data[i,j] <=high):
                    alert = "med"
                    MED.append([j , i , data[i,j], encoder[i]])
                    
                else:
                    alert = None

        #delete first entry of lists which is blank
        del HIGH[0]
        del LOW[0]
        del MED[0]

        h1 = len(HIGH)
        m1 = len(MED)
        l1 = len(LOW)

        #create 2-d numpy arrays and copy list data into arrays
        h = np.zeros((h1,4))
        m = np.zeros((m1,4))
        l = np.zeros((l1,4))

        for i in range(h1):
            for j in range(4):
                h[i,j] = HIGH[i][j]

        for i in range(l1):
            for j in range(4):
                l[i,j] = LOW[i][j]

        for i in range(m1):
            for j in range(4):
                m[i,j] = MED[i][j]

        #sort all numpy arrays in descending order of sensor values
        h[h[:,2].argsort()][::-1].astype(int)
        m[m[:,2].argsort()][::-1].astype(int)
        l[l[:,2].argsort()][::-1].astype(int)

        print("Data processed succesfully")
        #put numpy arrays into table widget

        table = ttk.Treeview(self.frame2)
        table['columns'] = ('id1', 'index1', 'value1', 'pos1','id2', 'index2', 'value2', 'pos2','id3', 'index3', 'value3', 'pos3' )

        vsb = ttk.Scrollbar(orient="vertical",
            command=table.yview)

        hsb = ttk.Scrollbar(orient="horizontal",
            command=table.xview)

        wid = (self.x - 20)//13

        table.heading("#0", text='')
        table.column("#0", anchor='center', width=0)

        table.heading('id1', text='ID')
        table.column('id1', anchor='center', width=wid)
        table.heading('id2', text='ID')
        table.column('id2', anchor='center', width=wid)
        table.heading('id3', text='ID')
        table.column('id3', anchor='center', width=wid)

        table.heading('index1', text='INDEX')
        table.column('index1', anchor='center', width=wid)
        table.heading('index2', text='INDEX')
        table.column('index2', anchor='center', width=wid)
        table.heading('index3', text='INDEX')
        table.column('index3', anchor='center', width=wid)

        table.heading('value1', text='Value')
        table.column('value1', anchor='center', width=wid)
        table.heading('value2', text='Value')
        table.column('value2', anchor='center', width=wid)
        table.heading('value3', text='Value')
        table.column('value3', anchor='center', width=wid)

        table.heading('pos1', text='POS')
        table.column('pos1', anchor='center', width=wid)
        table.heading('pos2', text='POS')
        table.column('pos2', anchor='center', width=wid)
        table.heading('pos3', text='POS')
        table.column('pos3', anchor='center', width=wid)

        






        table.place(x=0,y=0)

