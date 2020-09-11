#Add imports here
import time
import pygame as pg
from random import *
from social_class import *
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
rK = 50 #K+all modfiers 

#Set-Up
cGrowth = cGrowth+(bGrowth*(pg+gm-dm))
bGrowth = default_growth*(pg+gm-dm)

localtime = time.asctime( time.localtime(time.time()) )
file =open ("save_file.csv", "w", newline='')
file.write("Simulation from the "+str(localtime)+";;Total Timesteps;"+'\n')
file.write("Month: "+str(month)+" Year: "+ str(year)+';')
file.write("Population: "+";"+str(tts)+";"+ str(P)+'\n')
#file.write("Population: "+";"+ str(P)+";"+str(tts)+'\n')
print("Month: "+str(month)+" Year: "+ str(year))
print("Population: " + str(P)+"K")
print("Growth: "+str(bGrowth))
#print("Pop progress: "+str(cGrowth))

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

    print("")

    #Events
    if events == True: #Events and similar things
        #Reduce Pop Growth with larger populations
        dm=(P/K)
    
    #Time Keeper
    if month == 12:
        month=1
        year=year+1

    else:
        month=month+1

    #Printer
    if year == end_year:
        #Write into save_file.txt
        file.write("Month: "+str(month)+" Year: "+ str(year)+';')
        file.write("Population: "+";"+str(tts)+";"+ str(P)+'\n')
        file.write("Simulation has Ended"+'\n')
        localtime = time.asctime( time.localtime(time.time()) )
        file.write("Simulation from the "+str(localtime))
        file.close()
        #print in the Shell
        print("Month: "+str(month)+" Year: "+ str(year))
        print("Population: " + str(P)+"K")
        print("Growth: "+str(bGrowth))
        print("Simulation has Ended")
        running = False
    else:
        #Write into save_file.txt
        file.write("Month: "+str(month)+" Year: "+ str(year)+';')
        file.write("Population: "+";"+str(tts)+";"+ str(P)+'\n')
        #print in the Shell
        print("Month: "+str(month)+" Year: "+ str(year))
        print("Population: " + str(P)+"K")
        print("Growth: "+str(bGrowth))
        if go_normal == True:
            time.sleep(1)
        if go_fast == True:
            time.sleep(0.5)
        if go_very_fast == True:
            time.sleep(0.25)
        else:
            pass
