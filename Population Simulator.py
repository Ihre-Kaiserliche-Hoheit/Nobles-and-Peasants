#Add imports here
import time
from random import *
from social_class import *

#Simulation Status
running = True
go_fast = False
go_very_fast = True

#Time
year = 1
decade_counter = 1
end_year = 100

#Population and Social Classes
#Plebs
social_class.plebs = social_class()

social_class.plebs.r = 0.5  #(r = Growth) modifie this number to increase growth speed
social_class.plebs.K = 2000 #Maximum supstinable population
   
social_class.plebs.gen_0 = 0 #Newborn
social_class.plebs.gen_1 = 0 #Children&Teens
social_class.plebs.gen_2 = 90 #Young Adults
social_class.plebs.gen_3 = 10 #Adults
social_class.plebs.gen_4 = 0 #Seniors

social_class.plebs.new_P = 0
social_class.plebs.P = 100
social_class.plebs.old_P = 0
social_class.plebs.randomDeaths = 0
social_class.plebs.growth = 0

death = 0

#Other
e = 2.71828

#Start Numbers get printed
social_class.plebs.P = social_class.plebs.gen_0+social_class.plebs.gen_1+social_class.plebs.gen_2+social_class.plebs.gen_3+social_class.plebs.gen_4
print("Year: "+ str(year))
print("Population: " + str(social_class.plebs.P))
print("Growth: "+str(social_class.plebs.growth))

while running == True:

    #Importand Calculation Stuff
    #Date Updater
    year = year+1
    decade_counter = decade_counter+1

    if decade_counter == 10:

        #Population
        social_class.plebs.old_P = social_class.plebs.P
        social_class.plebs.P = round(social_class.plebs.K/(1+((social_class.plebs.K-social_class.plebs.P)/social_class.plebs.P*e**(social_class.plebs.r*10))))
    
        #Get amount of new pop
        social_class.plebs.new_P = social_class.plebs.old_P-social_class.plebs.P #Hope this works!
        
        social_class.plebs.randomDeaths = randint(0,10)
        social_class.plebs.randomDeaths = social_class.plebs.randomDeaths/10
        social_class.plebs.randomDeaths = round(social_class.plebs.randomDeaths, 2)
        social_class.plebs.randomDeaths = social_class.plebs.new_P*social_class.plebs.randomDeaths
        social_class.plebs.new_P = round(social_class.plebs.new_P-social_class.plebs.randomDeaths)
        
        #Move Gens
        social_class.plebs.death = social_class.plebs.gen_4
        social_class.plebs.gen_4 = social_class.plebs.gen_3
        social_class.plebs.gen_3 = social_class.plebs.gen_2
        social_class.plebs.gen_2 = social_class.plebs.gen_1
        social_class.plebs.gen_1 = social_class.plebs.gen_0
        social_class.plebs.gen_0 = social_class.plebs.new_P

        decade_counter = 0

        social_class.plebs.P = social_class.plebs.gen_0+social_class.plebs.gen_1+social_class.plebs.gen_2+social_class.plebs.gen_3+social_class.plebs.gen_4
        social_class.plebs.growth = social_class.plebs.new_P-social_class.plebs.death

    else:
        social_class.plebs.new_P = 0
        social_class.plebs.death = 0
        social_class.plebs.growth = 0
 
    #Printer goes prrrrrrrr

    print("Year: "+ str(year))

    if year == end_year:
        print("Population:" + str(social_class.plebs.P))
        print("Growth: "+str(social_class.plebs.growth))
        print("The set end year was reached and the simulation ended")
        running = False
        
    else:
        print("Population:" + str(social_class.plebs.P))
        print("Growth: "+str(social_class.plebs.growth))
        
        if go_fast == True:
            time.sleep(0.5)

        if go_very_fast == True:
            time.sleep(0.1)
            
        else:
            time.sleep(1)

else:
    print("SIMULATION ENDED AFTER "+str(year)+" YEARS")
