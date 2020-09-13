#This code creates, updates and kills off characters
#Imports
import time
from random import *

#Time Values
month = 1
year = 1
end_year = 10
tts = 1

running = True

class person():
    name = "Adam"
    surname = ""
    female = False
    birth_date = 1
    age = 1
    father = 0
    mother = 0
    spouse = 0

while running == True:
    tts = tts+1
    if month == 12:
        month = 1
        year = year+1
    else:
        month = month+1
    person.age = tts-person.birth_date
    print(tts)
    print("Age: "+ str(person.age))
