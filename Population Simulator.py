#Add imports here
import time
import random
from Tkinter import *

#add new values here
#Time
day = 1
month = 1
year = 1
total_days = 1

#Population
P = 2500 #Population
P2 = 0
New_P = 0
Growth = 0

r = 1.25  #(r = Growth) modifie this number to increase growth speed
K = 10000 #Maximum supstinable population
euler = 2.71828

Gen_1 = 2000 #Children&Teens
Gen_2 = 1000 #Young Adults
Gen_3 = 500 #Old Adults
Gen_4 = 200 #Old People
Death = 100 #Deadpeople


#Other
running = True

#Start Numbers get printed
P = Gen_1 + Gen_2 + Gen_3 + Gen_4
Adults = Gen_2 + Gen_3
print("Year: "+ str(year)+" Month: " +str(month)+" Day: "+str(day)+" (Total days: "+str(total_days)+")")
print("Population: " + str(P2))
print(Growth)
print(Death)

while running == True:

    #Importand Calculation Stuff
    #Date Updater
    total_days = total_days+1
    if day == 3:
        day = 1
        month = month+1

        #Population
        P2 = P
        Adults = Gen_2 + Gen_3
        P = K/(1+((K-P)/P)*euler**(-r))
        P = round(P)
        #Get amount of new pop
        Growth = P-P2
        #Move Gens
        Death = Gen_4
        Gen_4 = Gen_3
        Gen_3 = Gen_2
        Gen_2 = Gen_1
        Gen_1 = New_P
        P = Gen_1 + Gen_2 + Gen_3 + Gen_4
        
    if month == 4:
        month = 1
        year = year+1
        
    else:
        day = day+1
        #month = month+1

    #Printer goes prrrrrrrr
    print("Year: "+ str(year)+" Month: " +str(month)+" Day: "+str(day)+" (Total days: "+str(total_days)+")")
    if P <= 0:
         print("Population is Zero, nobody is left to reproduce")
         running = False   
    else:
        print("Population:" + str(P))
        print("Births: "+str(Growth))
        print("Deaths: "+str(Death))
        time.sleep(1)

else:
    print("Simulation Failed")
