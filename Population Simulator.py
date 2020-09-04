#Add imports here
import time
from random import *

#Time
year = 1
decade_counter = 1
end_year = 100

#Population
r = 0.5  #(r = Growth) modifie this number to increase growth speed
K = 2000 #Maximum supstinable population
euler = 2.71828
    
Gen_0 = 0 #Newborn
Gen_1 = 0 #Children
Gen_2 = 90 #Young Adults
Gen_3 = 10 #Adults
Gen_4 = 0 #Seniors

New_P = 0
P = 1500
P2 = 0
Death = 0

randomDeaths = 0
Childdeaths = 0
Growth = 0

#Other
running = True

#Start Numbers get printed
P = Gen_0+Gen_1+Gen_2+Gen_3+Gen_4
print("Year: "+ str(year))
print("Population: " + str(P))
print("Growth: "+str(Growth))

while running == True:

    #Importand Calculation Stuff
    #Date Updater
    year = year+1
    decade_counter = decade_counter+1

    if decade_counter == 10:

        #Population
        P2 = P
        P = round(K/(1+((K-P)/P*euler**(r*10))))
    
        #Get amount of new pop
        New_P = P2-P #Hope this works!
        
        randomDeaths = randint(0,10)
        randomDeaths = randomDeaths/10
        randomDeaths = round(randomDeaths, 2)
        randomDeaths = New_P*randomDeaths
        New_P = round(New_P-randomDeaths)
        
        #Move Gens
        Death = Gen_4
        Gen_4 = Gen_3
        Gen_3 = Gen_2
        Gen_2 = Gen_1
        Gen_1 = Gen_0
        Gen_0 = New_P

        decade_counter = 0

        P = Gen_0+Gen_1+Gen_2+Gen_3+Gen_4
        Growth = New_P-Death
        
        

    #elif decade_counter == 5:
    #    Death = (Gen_4/2)+(Gen_3/4)
    #    Gen_3 = Gen_3/4
    #    Gen_3 = round(Gen_3)
    #    Gen_4 = Gen_4/2
    #    Gen_4 = round(Gen_4)
    #    Death = round(Death)
    #    
    #    #Update P
    #    P = Gen_0+Gen_1+Gen_2+Gen_3+Gen_4


    else:
        New_P = 0
        Death = 0
        Growth = 0
 
    #Printer goes prrrrrrrr

    print("Year: "+ str(year))
    if P <= 0:
        print("Population is Zero, nobody is left to reproduce")
        running = False

    if year == end_year:
        print("Population:" + str(P))
        print("Growth: "+str(Growth))
        print("The set end year was reached and the simulation ended")
        running = False
        
    else:
        print("Population:" + str(P))
        print("Growth: "+str(Growth))
        time.sleep(1)


else:
    print("SIMULATION ENDED AFTER "+str(year)+" YEARS")
