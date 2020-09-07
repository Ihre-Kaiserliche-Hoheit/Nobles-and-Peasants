#To-Do List
#-Slim down the population code

#Add imports here
import time
from random import *
from social_class import *

#Simulation Status
running = True
go_fast = False
go_very_fast = True
too_many_eater = False

#Stuffy Stuff
e = 2.71828

#Time
year = 1
decade_counter = 1
end_year = 100

#Population and Social Classes
total_P = 0
#Plebs
social_class.plebs = social_class()
social_class.burgher = social_class()

social_class.plebs.r = 0.25  #(r = Growth) modifie this number to increase growth speed
social_class.plebs.K = 5000 #Maximum supstinable population
   
social_class.plebs.gen_0 = 0 #Newborn
social_class.plebs.gen_1 = 500 #Children&Teens; This and Young Adults need to have population in them or a "division by zero"-error will appear!
social_class.plebs.gen_2 = 500 #Young Adults
social_class.plebs.gen_3 = 0 #Adults
social_class.plebs.gen_4 = 0 #Seniors

social_class.plebs.new_P = 0
social_class.plebs.P = 500
social_class.plebs.old_P = 0
social_class.plebs.adults = 0

social_class.plebs.randomDeaths = 0
social_class.plebs.growth = 0

#Birth and Death
growth = 0
death = 0

#Start Numbers get printed
social_class.plebs.P = social_class.plebs.gen_0+social_class.plebs.gen_1+social_class.plebs.gen_2+social_class.plebs.gen_3+social_class.plebs.gen_4

total_P = social_class.plebs.P
growth = social_class.plebs.growth

#Update K

print("Year: "+ str(year))
print("Population: " + str(total_P))
print("Peasants: "+str(social_class.plebs.P))
print("Growth: "+str(growth))

while running == True:

	#Importand Calculation Stuff
	#Date Updater
	year = year+1
	decade_counter = decade_counter+1

	if decade_counter == 10:
	
	#Plebs
		#Population
		social_class.plebs.adults = social_class.plebs.gen_2 + social_class.plebs.gen_3
		social_class.plebs.old_P = social_class.plebs.P
		social_class.plebs.new_P = social_class.plebs.K/(1+((social_class.plebs.K-social_class.plebs.adults)/social_class.plebs.adults*e**social_class.plebs.r))
	
		#Get amount of new pop
		#social_class.plebs.new_P = social_class.plebs.old_P-social_class.plebs.P #Hope this works!
		
		social_class.plebs.randomDeaths = randint(0,10)
		social_class.plebs.randomDeaths = social_class.plebs.randomDeaths/100
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

		social_class.plebs.gen_3 = round(social_class.plebs.gen_3*0.8)
		social_class.plebs.gen_4 = round(social_class.plebs.gen_4*0.5)
	

		social_class.plebs.P = social_class.plebs.gen_0+social_class.plebs.gen_1+social_class.plebs.gen_2+social_class.plebs.gen_3+social_class.plebs.gen_4
		social_class.plebs.growth = social_class.plebs.new_P-social_class.plebs.death

		#Update of general Values
		decade_counter = 0
		total_P = social_class.plebs.P
		growth = social_class.plebs.growth
		
	else:
		#Plebs
		social_class.plebs.new_P = 0
		social_class.plebs.death = 0
		social_class.plebs.growth = 0

		#General
		growth = 0

		social_class.plebs.P = social_class.plebs.gen_0+social_class.plebs.gen_1+social_class.plebs.gen_2+social_class.plebs.gen_3+social_class.plebs.gen_4
		total_P = social_class.plebs.P
		 
	#Printer goes prrrrrrrr
	print("Year: "+ str(year))

	if year == end_year:
		print("Population: " + str(total_P))
		print("Peasants: "+str(social_class.plebs.P))
		print("Growth: "+str(growth))
		print("The set end year was reached and the simulation ended")
		running = False
		
	else:
		print("Population: " + str(total_P))
		print("Peasants: "+str(social_class.plebs.P))
		print("Growth: "+str(growth))

		if go_fast == True:
			time.sleep(0.5)

		if go_very_fast == True:
			time.sleep(0.1)
			
		else:
			time.sleep(1)

else:
	print("SIMULATION ENDED AFTER "+str(year)+" YEARS")
