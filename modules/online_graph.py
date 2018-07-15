import requests
import time
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime
import matplotlib.animation as animation
from matplotlib import style

class online_graph:

    def __init__(self):
        
        #number of plots 2 : first for 4 ldr and second for 4 pzt sensor
        fig, (ax1, ax2) = plt.subplots(2, sharey=True, sharex=True)
        fig.suptitle('Sensor Data Visualization')
        fig.subplots_adjust(hspace=0.1)
        
        #save data received online in fname
        time_stamp = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
        fname = '../Logs/Z_Output'+time_stamp+'.txt'

        #sensor data in sensor 1-8, encoder data in dist and time in time_t variable
        global sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, dist, time_t

        #display 40 values at a time on screen
        dist = [0]*40
        time_t = [0]*40
        sensor1 = [0]*40
        sensor2 = [0]*40
        sensor3 = [0]*40
        sensor4 = [0]*40
        sensor5 = [0]*40
        sensor6 = [0]*40
        sensor7 = [0]*40
        sensor8 = [0]*40

        #make a file for storing the online data
        text_file = open(fname,"a")
        text_file.write("---------------------START NEW RUN-------------------------\n")

        #main plotting function ecursivelycalled by matplotlib animation function
        def online_plot(i):
            #flag=1

            #8 sensor + encoder data + time
            num_sensors = 10

            #fetch data from url on localserver of ESP
            
            #r = requests.get("http://192.168.43.197")
            #s = r.text

            #testing
            file_name = '../dev/Gail_PHMR_Robot.html'
            s = open(file_name,'r').read()

            #sensor values were put inside <h4> tag, extract vallues between <h4> tag
            first="<h4>"
            last="</h4>"
            start = s.rindex(first)+len(first)
            end = s.rindex(last, start)
            req = s[start:end]
            l = req.split(',')

            global sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, dist, time_t

            #check if all 10 values are put by esp on server
            if(len(l)!=num_sensors):
                print("data erorr occurred")

                #In case of data error copy the previous data as new data in case of data error
                x11 = sensor1[39]; x21 = sensor2[39]; x31 = sensor3[39]; x41 = sensor4[39]; 
                x51 = sensor5[39]; x61 = sensor6[39]; x71 = sensor7[39]; x81 = sensor8[39]
          
            else:
                #print data on terminal
                print(l)

                #remove /r/n from the end of string 
                del l[-1:-2]

                #convert string values into numbers
                l = [(int(i)) for i in l]

                #convert reading into Volts by multiplying all sensor values with vf
                vf = 5/1024
                x11 = l[0]*vf; x21 = l[1]*vf; x31 = l[2]*vf; x41 = l[3]*vf;
                x51 = l[4]*vf; x61 = l[5]*vf; x71 = l[6]*vf; x81 = l[7]*vf
                x_dist = l[8]
                x_time = l[9]

            #write the extracted data on local file
            text_file.write(req)
            text_file.write("\n")

            #implementation of dynamic plot
            fig.suptitle('Online Sensor Data Visualization: T = '+str(x_time/1000 )+' sec.')
            fig.subplots_adjust(hspace=0.1)

            #update sensor values by popping the front and pushing new values at end
            del sensor1[:1]; sensor1.append(x11);       
            del sensor2[:1]; sensor2.append(x21); 
            del sensor3[:1]; sensor3.append(x31); 
            del sensor4[:1]; sensor4.append(x41); 
            del sensor5[:1]; sensor5.append(x51); 
            del sensor6[:1]; sensor6.append(x61); 
            del sensor7[:1]; sensor7.append(x71); 
            del sensor8[:1]; sensor8.append(x81); 
    
            #update encoder values on x-axis in cm.
            dist1 = round((x_dist*np.pi*5)/(2400), 3) 

            del dist[:1]; dist.append(dist1);

            #update time 
            del time_t[:1]; time_t.append(x_time)

            #clear the plots for re-drawing
            ax1.clear()
            ax2.clear()
            
            
            #make x-axis variable of length 40 as there are 40 values in sensor array at a time 
            x_axis = [i for i in range(40)]
            
            #plot LED-LDR data
            ax1.plot(x_axis,sensor1,Linewidth=2.0,label="LDR1")
            ax1.plot(x_axis,sensor2,Linewidth=2.0,label="LDR2")
            ax1.plot(x_axis,sensor3,Linewidth=2.0,label="LDR3")
            ax1.plot(x_axis,sensor4,Linewidth=2.0,label="LDR4")
            ax1.legend(loc="upper right", ncol=4)
            
            #plot PZT Data
            ax2.plot(x_axis,sensor5,Linewidth=2.0,label="PZT1")
            ax2.plot(x_axis,sensor6,Linewidth=2.0,label="PZT2")
            ax2.plot(x_axis,sensor7,Linewidth=2.0,label="PZT3")
            ax2.plot(x_axis,sensor8,Linewidth=2.0,label="PZT4")
            ax2.legend(loc="upper right", ncol=4)
            
            axarr = [ax1,ax2]

            #put x-label only in outer x-axis
            for ax in axarr:
                ax.label_outer()

            #add axis information in graph
            ax1.grid(color='k', linestyle='-.', linewidth=0.2)
            ax1.set_ylabel("Sensor Output [in Volts]")       
            ax1.set_ylim([0,5])  
            ax1.set_xticklabels(dist, rotation='vertical')
            
            ax2.grid(color='k', linestyle='-.', linewidth=0.2)
            ax2.set_xlabel("Distance (in meters)")
            ax2.set_ylabel("Sensor Output [in Volts]")       
            ax2.set_ylim([0,5])  
            ax2.set_xticklabels(dist, rotation=70)
    
            

        #call animation function for real time plot    
        ani = animation.FuncAnimation(fig, online_plot, frames=None)
        plt.show()
