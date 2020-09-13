#Add imports here
import time
from random import *
import csv

#Simulation Status
running = True
go_normal = False
go_fast = False
go_very_fast = False
events = True
#Time
tts = 1 #Totat Timesteps
month = 1
year = 1
end_year = 10
#Amount of Pops & related stuff; 1 Pop = 1k People
P = 1
cGrowth = 0
pg = 1
dm = 0
gm = 0
bGrowth = 100
default_growth = 100
n_growth = 0
K = 50

#Set-Up
cGrowth = cGrowth+(bGrowth*(pg+gm-dm))
bGrowth = default_growth*(pg+gm-dm)

def write_file(tts, P, month, year):
    #Write into save_file.txt
    file.write(str(month)+";"+str(year)+";"+str(tts)+";"+ str(P)+'\n')
def print_data(month, year, P, bGrowth):
    print("Month: "+str(month)+" Year: "+ str(year))
    print("Population: " + str(P)+"K")
    print("Growth: "+str(bGrowth))

localtime = time.asctime( time.localtime(time.time()) )
file =open ("save_file.csv", "w", newline='')
file.write("Simulation started on the "+str(localtime)+"\n"+"Month;Year;Total Timesteps;Pops"+'\n')
write_file(tts, P, month, year)
print_data(month, year, P, bGrowth) #print to the Shell

#Running Code
while running == True:
    tts = tts+1
    #Census
    bGrowth = default_growth*(pg+(gm-dm))
    round(bGrowth)
    if cGrowth >= 1000:
        n_growth=round(cGrowth/1000)
        cGrowth = cGrowth-(n_growth*1000)
        P=P+n_growth
    else:
        cGrowth = cGrowth+bGrowth

    print("")#To make printed output easy to read
    
    if events == True: #Events and similar things
        dm=(P/K)    #Reduce Pop Growth with larger populations
    else:
        pass
    #Time Keeper Code
    if month == 12:
        month=1
        year=year+1
        if year != end_year:
            write_file(tts, P, month, year) #Write into save_file.txt
    else:
        month=month+1

    #Printer
    if year == end_year:
        write_file(tts, P, month, year) #Write into save_file.txt
        file.write("Simulation has Ended"+'\n')
        localtime = time.asctime( time.localtime(time.time()) )
        file.write("Simulation ended on the "+str(localtime))
        file.close()
        print_data(month, year, P, bGrowth) #print to the Shell
        print("Simulation has Ended")
        running = False
    else:
        print_data(month, year, P, bGrowth) #print to the Shell
        if go_normal == True:
            time.sleep(1)
        if go_fast == True:
            time.sleep(0.5)
        if go_very_fast == True:
            time.sleep(0.25)
        else:
            pass
