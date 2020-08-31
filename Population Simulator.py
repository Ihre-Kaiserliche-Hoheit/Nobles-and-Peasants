#Add imports here
import time
import random

#add new values here
#Time
day = 1
month = 1
year = 1
total_days = 1

#Population
P = 500 #Population
P2 = 0
P3 = 0
New_P = 0
r = 1  #(r = Growth) modifie this number to increase growth speed
K = 10000 #Maximum supstinable population
euler = 2.71828

Gen_1 = 0 #Children&Teens
Gen_2 = 0 #Young Adults
Gen_3 = 0 #Old Adults
Gen_4 = 0 #Old People
Death = 0 #Deadpeople

#Other
running = True

#Start Numbers get printed
print("Year: "+ str(year)+" Month: " +str(month)+" Day: "+str(day)+" (Total days: "+str(total_days)+")")
print("Population: " + str(P2))
print(New_P)

while running == True:

    #Importand Calculation Stuff
    #Date Updater
    total_days = total_days+1
    #if day == 7:
        #day = 0
        #month = month+1
        
    if month == 4:
        month = 1
        year = year+1
        
    else:
        #day = day+1
        month = month+1

        #Population
        P2 = P
        P3 = Gen_2 + Gen_3
        P = K/(1+((K-P)/P)*euler**(-r))
        P = round(P)
        #Get amount of new pop
        New_P = P-P2
        #Move Gens
        Death = Gen_4
        Gen_4 = Gen_3
        Gen_3 = Gen_2
        Gen_2 = Gen_1
        Gen_1 = New_P
        P = Gen_1 + Gen_2 + Gen_3 + Gen_4

    
    #Printer goes prrrrrrrr
    print("Year: "+ str(year)+" Month: " +str(month)+" Day: "+str(day)+" (Total days: "+str(total_days)+")")
    if P <= 0:
         print("Population is Zero, nobody is left to reproduce")
         running = False   
    else:
        print("Population:" + str(P))
        print("Growth: "+str(New_P))
        print("Deaths: "+str(Death))
        time.sleep(1)

else:
    print("Simulation Failed")
