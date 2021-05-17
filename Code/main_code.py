"""
TODO:
    General
        Fix any remaining bugs
        Fine tune systems
        Burn Tech-Heresy at every possible moment
"""


#NOTE:
#I likely don't know either how half of this works in a few weeks - Kaiser

#Custom Imports
import custom_lib as cl
import gedcom_converter as gc
import map_code as map_c
from relationship_finder import is_sibling, is_cousin
from action_weights import weight_age, weight_relation
from calc import calc_death_chance

import random as r
import math as m


#Values to tweak and stuff
#If not changed the Seed of the randomness will be the current date
Seeder = cl.get_time() #Seed for the randomness of the simulation, change this every run!
r.seed(Seeder) #Set seed for repeatable results
#Change values to the setting ones
printing = True

settings = cl.txt_to_list("../Input/Settings.txt")
settings.pop(0)
seed = int(settings[0])
k = int(settings[1])
life_expectantcy = int(settings[2])
preg_tweak = int(settings[4])
growth_influence_1 = int(settings[5])
start_year = int(settings[6])
end_year = int(settings[7])
del(settings)

#Values you shouldn't touch
year = start_year #Current year
world = map_c.region()
world.set_up_map()

total_population = [] #List of EVERY person that ever lived
queue = [] #Acting queue for characters
avaible_males = [] #List of fertil and unmarried men
avaible_females = [] #List of fertil and unmarried women

p = seed #current population count

male_names = []
female_names = []
lastnames = []

male_names = cl.txt_to_list("../Input/Male.txt")
female_names = cl.txt_to_list("../Input/Female.txt")
lastnames = cl.txt_to_list("../Input/Lastname.txt")

e = m.e #Eulers number


#Person class
class person():
    def __init__(self):
        self.uid = None #The id of a character
        self.name = ""
        self.surname = ""
        self.sex = None  #0 = Man, 1 = Woman
        self.birth_date = None
        self.birth_place = ""
        self.age = 0
        self.death_date = None
        self.death_place = ""
        self.alive = True
        self.location = []

        self.father = []
        self.mother = []
        self.spouse = []
        self.children = []
        self.post_pregnancy_break = 0 #How long until a woman can have kids again

        self.grandparents = [] #A list of all their grandparents
        self.great_grandparents = [] #A list of all their great grandparents

    def update(self, kr):
        self.age +=1
        if 18 < self.age and len(self.spouse) == 0:
            find_spouse(self)

        if 1 == len(self.spouse) and self.sex == 1 and self.age < 40:
            spouse = self.spouse[0]
            if spouse.alive == True: #FIXED Find out why this kills the population after ~100-200 years
                rand_value = r.random()*growth_influence_1
                self.post_pregnancy_break -=1
                if self.post_pregnancy_break < 0:
                    self.post_pregnancy_break = 0

                if rand_value < preg_tweak*kr and 0 <= self.post_pregnancy_break:
                    self.have_kid(self, self.spouse[0])

        self.death() #Looks if they die today

    def create(self):
        self.uid = len(total_population)+1
        self.birth_date = year
        self.sex = r.randint(0, 1)
        set_whole_name(self)

    def birth(self, mother, father):
        #Create child
        child = person()
        child.create()

        #Add parent-child relations
        parent_child(mother, child)
        parent_child(father, child)

        #Set grandparents and great grandparents
        child.update_ancestors(mother, father, child)

        #Set location
        child.location = mother.location
        loc = child.location[0]
        child.birth_place = loc.name

        #Add to population list
        add_to_population(child)

        #Post-pregnancy break
        mother.post_pregnancy_break = r.randint(1, 2)

    def update_ancestors(self, mother, father, child):
        child.grandparents = list()
        child.grandparents = mother.mother + mother.father + father.mother + father.father
        child.great_grandparents = list()
        child.great_grandparents = list(mother.grandparents) + list(father.grandparents)
        child.grandparents = set(child.grandparents)
        child.great_grandparents = set(child.great_grandparents)
        pass

    def have_kid(self, mother, father):
        if mother.post_pregnancy_break <= 0:
            mother.birth(mother, father)

    def death(self):
        age_dif = self.age - life_expectantcy #Gets how far above/below they are
        location = self.location[0]
        death_chance = calc_death_chance(life_expectantcy, self.age, location.local_child_mortality, len(location.inhabitans), location.effectiv_k)
        #if the value is below death_chance they die
        death_roll = round(r.random(), 8)
        if death_roll <= death_chance:
            #You died, and now get gud
            self.death_date = year
            self.alive = False
            location.inhabitans.remove(self)
            self.death_place = location.name

#All the other stuff
def parent_child(parent, child):
    parent.children.append(child)
    if parent.sex == 0:
        child.father.append(parent)
    else:
        child.mother.append(parent)

def find_spouse(searcher):
    pool_of_possible_spouses = list()
    location = searcher.location[0]
    #Creates a ~hopefully~ fully unqiue list of people
    try:
        if searcher.sex == 0:
            pool_of_possible_spouses = cl.create_random_list_from(location.avaible_females, 20)
        else:
            pool_of_possible_spouses = cl.create_random_list_from(location.avaible_males, 20)

    except cl.EmptyListError:
        pass #Just ignore the error

    if 0 < len(pool_of_possible_spouses):
        #Searches for the best fit among the random people chosen
        best_fit = [""]
        best_value = -1
        for i in range(len(pool_of_possible_spouses)):
            other = pool_of_possible_spouses[i]
            value = assigne_spouse_value(searcher, other)
            if best_value < value and 17 < other.age and len(other.spouse) == 0 and len(searcher.spouse) == 0:
                #                                           ^                          ^
                #                                          For some fucking reason this fixes the population death bug
                best_fit.clear()
                best_fit.append(other)
                best_value = value
        if best_fit[0] != "":
            fit = best_fit[0]
            marrige(searcher, fit)

def marrige(partner1, partner2):
    partner1.spouse.append(partner2)
    partner2.spouse.append(partner1)
    if partner1 == 0:
        avaible_males.remove(partner1)
        avaible_females.remove(partner2)
    elif partner1 == 1:
        avaible_males.remove(partner2)
        avaible_females.remove(partner1)

def assigne_spouse_value(searcher, other):
    value = 0
    #Add new factors for spouse choice here
    value = value + weight_age(other, "medium") + weight_relation(searcher, other)

    return(value)

def from_thin_air(person):
    #Creates person
    person.create()

    #Set birth year
    rage = r.randint(17, 23)
    person.birth_date = year-rage
    person.age = rage

    #Set location
    location = world.places[0]
    person.location.append(location)
    person.birth_place = str(location.name)

    #Add to population lists
    add_to_population(person)

def set_name(sex):
    name = ""
    if sex == 0:
        name = r.choice(male_names)
    else:
        name = r.choice(female_names)

    return(name)

def set_surname(child, father, mother):
    ran = r.randint(0, 10)
    surname = ""

    if 3 < ran < 9:
        #Most people just take the lastname of their father
        surname = father.surname
    elif 9 < ran < 11 and "-" not in father.surname and "-" not in mother.surname:
        #Some have both their mothers and fathers lastname
        surname = str(father.surname) + "-" + str(mother.surname)

    if surname.startswith("-"):
        #Some have lastnames that start weirdly and need to be PURGED
        surname = surname.strip("-")

    if surname == "":
        #And some are just poor bastards without a lastname
        surname = random_surname()

    return(surname)

def random_surname():
    surname = r.choice(lastnames)

    return(surname)

def set_whole_name(person):
    person.name = set_name(person.sex)
    try:
        person.surname = set_surname(person, person.father[0], person.mother[0])
    except IndexError:
        person.surname = random_surname()

def add_to_population(person):
    #Add to both lists, cuz it is easy to have one function that does both for me
    location = person.location[0]
    total_population.append(person)
    location.inhabitans.append(person)

for i in range(seed):
    #Create starting population
    new_person = person()
    from_thin_air(new_person)

census = open("census.csv", "w")
census.write("Year;")
for i in range(len(world.places)):
    place = world.places[i]
    census.write(str(place.name) + ";")
census.write("\n")
census.write(str(start_year) + ";\n")

while year < end_year:
    #Simulation cycle after the creation
    year +=1
    p = world.return_population()
    census.write(str(year) + ";")

    for i in range(len(world.places)):
        place = world.places[i]
        place.update()

    for i in range(len(world.places)):
        #This second loop is done because the values change during the first
        #So this prevents inconsitencies in the data
        place = world.places[i]
        census.write(str(place.return_population()) + ";")
    census.write("\n")
    if printing == True:
        print("Year " + str(year))
        print(p)

#From here on we have the data export code
file = open("raw_output.txt", "w")
file.write("Seed(" + str(Seeder) + ") \n"
           "ID; Name; Surname; Sex; Father; Mother; Spouse; Children; Birth; Death; Age; \n")

for i in range(len(total_population)):
    person = total_population[i]
    children = person.children
    id_list = []
    for ii in range(len(children)):
        child = children[ii]
        id_list.append(child.uid)
    #If you hate this many try-except blocks do a better job
    try:
        father = person.father[0]
        father_id = father.uid
    except IndexError:
        father_id = ""
    try:
        mother = person.mother[0]
        mother_id = mother.uid
    except IndexError:
        mother_id = ""
    try:
        spouse = person.spouse[0]
        spouse_id = spouse.uid
    except IndexError:
        spouse_id = ""
    file.write(str(person.uid) + ";" + str(person.name)  + ";" + str(person.surname)  + ";" + str(person.sex) + ";" + str(father_id)  + ";" + str(mother_id) + ";" + str(spouse_id) + ";" + str(id_list) + ";" + str(person.birth_date) + ";" + str(person.death_date) + ";" + str(person.birth_place) + ";" + str(person.death_place) + ";"  + str(person.age) + "; \n")

file.close()
census.close()
gc.converter()

#Clean up, delets raw_output and moves the gedcom to the output folder
cl.delete_file("raw_output.txt")
cl.delete_file("census.csv")
cl.move_file("gedcom.ged", "../Output")
cl.rename_file("../Output/gedcom.ged", "../Output/"+Seeder+".ged")
print("Done, your gedcom is in the Output folder")
