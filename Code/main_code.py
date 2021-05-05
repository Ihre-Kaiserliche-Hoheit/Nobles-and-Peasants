"""
TODO:
    General
        Fix any remaining bugs
        Fine tune systems
        Burn Tech-Heresy at every possible moment

    Version ?.?
        System that auto prunes the family tree before converting it into a .ged?
"""

#NOTE:
#I likely don't know either how half of this works in a few weeks - Kaiser

#Custom Imports
import custom_lib as cl
import gedcom_converter as gc
import map_code as map_c


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
life_expecantcy_avg = int(settings[2])
infant_mortality = float(settings[3])
preg_tweak = int(settings[4])
growth_influence_1 = int(settings[5])
start_year = int(settings[6])
end_year = int(settings[7])


#Values you shouldn't touch
year = start_year #Current year
world = map_c.region()
world.set_up_map()

total_population = [] #List of EVERY person that ever lived
queue = [] #Acting queue for characters
avaible_males = [] #List of fertil and unmarried men
avaible_females = [] #List of fertil and unmarried women

p = seed #current population count
base_infant_mortality = infant_mortality #Base infant mortality, don't change directly or you may fuck stuff up

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

    def update(self, kr):
        self.age +=1
        if 18 < self.age and len(self.spouse) == 0:
            find_spouse(self)
        elif len(self.spouse) > 0 and self.sex == 1 and self.age < 40:
            rand_value = r.random()*growth_influence_1
            self.post_pregnancy_break -=1
            if self.post_pregnancy_break < 0:
                self.post_pregnancy_break = 0

            if rand_value < preg_tweak*kr and 0 <= self.post_pregnancy_break:
                self.have_kid(self, self.spouse[0])

        self.death() #Looks if they die today

    def birth(self, mother, father):
        #Create child
        child = person()
        child.uid = len(total_population)

        #Add parent-child relations
        parent_child(mother, child)
        parent_child(father, child)

        #Set values
        child.birth_date = year
        child.sex = r.randint(0, 1)
        set_whole_name(child)
        child.location = mother.location
        loc = child.location[0]
        child.birth_place = loc.name

        add_to_population(child)
        mother.post_pregnancy_break = r.randint(1, 3)

    def have_kid(self, mother, father):
        if mother.post_pregnancy_break <= 0:
            mother.birth(mother, father)

    def death(self):
        age_dif = self.age - life_expecantcy_avg #Gets how far above/below they are
        death_chance = calc_death_chance(age_dif)
        #if the value is below death_chance they die
        death_roll = round(r.random(), 8)
        if death_roll <= death_chance:
            #You died, and now get gud
            death(self)


#All the other stuff
def parent_child(parent, child):
    parent.children.append(child)
    if parent.sex == 0:
        child.father.append(parent)
    else:
        child.mother.append(parent)

def find_spouse(searcher):
    pool_of_possible_spouses = []
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
            if best_value < value:
                best_fit.clear()
                best_fit.append(other)
                best_value = value
        if best_fit[0] != "":
            marrige(searcher, best_fit[0])

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
    value = value + asses_age(other) + asses_relation(searcher, other)

    return(value)

def asses_age(other):
    #Older == Less likely to marry
    value = 0
    if 35 < other.age:
        value = value - 25

    elif other.age < 25:
        value += 10

    else:
        value += 2

    return(value)

def asses_relation(p1, p2):
    #Most people don't want to marry their siblings...
    value = 0
    try:
        if is_sibling(p1, p2) == True:
            #Yikes, we ain't in Alabama
            value = -50

        elif is_cousin(p1, p2) == True:
            #Habsburg, get the fuck out
            value = -25

        else:
            value = 10 #Should always be identical to the value in the except-block

    except IndexError: #Because the first gen has no parents
        value = 10

    #Maybe add more complex system for more distant relatives
    return(value)

def is_cousin(p1, p2):
    #Checks if p1 and p2 are cousins or not
    #I doubt this is the best way to do this function but I have no clue how to do it better
    f1 = p1.father[0]
    f2 = p2.father[0]
    m1 = p1.mother[0]
    m2 = p2.mother[0]

    if is_sibling(f1, f2) == True or is_sibling(m1, m2) == True or is_sibling(f1, m2) == True or is_sibling(f2, m1) == True:
        return True
    else:
        return False

def is_sibling(p1, p2):
    #Checks if p1 and p2 are siblins or not
    if p1.father[0] == p2.father[0] or p1.mother[0] == p2.mother[0]:
        return True
    else:
        return False

def from_thin_air(person):
    #For the set up only
    #Create child
    person.uid = len(total_population)
    #Set values
    rage = r.randint(17, 23)
    person.birth_date = year-rage
    person.age = rage
    person.sex = r.randint(0, 1)
    location = world.places[0]
    set_whole_name(person)
    person.location.append(location)
    person.birth_place = str(location.name)
    #Add to population lists
    add_to_population(person)

def death(person):
    #U ded
    person.death_date = year
    person.alive = False
    location = person.location[0]
    location.inhabitans.remove(person)
    person.death_place = location.name

def set_name(sex):
    name = ""
    if sex == 0:
        name = r.choices(male_names)

    else:
        name = r.choices(female_names)
    #Maybe adda list of gender-neutral names for the case this code fucks up? - Kaiser
    #Nah, this is fine - Steve
    name = name[0]
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
    surname = r.choices(lastnames)
    surname = surname[0]
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

def calc_death_chance(x): #x = age_dif
    A = x + life_expecantcy_avg
    #Calculates infant mortality, small spike in the first four or so years
    d1 = base_infant_mortality*e**((-5*(A))*(p/k))
    #Calculates liklyhood to die because of a critical code error in the code needed to survive - Kaiser
    #Normal people just call it death by natrual causes - Steve
    d2 = (50/(1+e**(-0.19*(x+8))))/100
    #More general causes of death like being crushed by a blue whale that fell from the sky - Kaiser
    #That isn't a normal cause of death - Steve
    d3 = (0.0004*A+0.00001)*e**(1-A/life_expecantcy_avg)
    dc = round(d1+d2+d3, 8) #Rounds to closes 7th diget after the point, cuz we love precision
    return(dc) #Gib me dat chance

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
        place = world.places[i]
        census.write(str(place.return_population()) + ";")
    census.write("\n")
    if printing == True:
        print("Year " + str(year))
        print(p)
    base_infant_mortality = base_infant_mortality*0.9 #Revise if tech is ever added

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
cl.move_file("gedcom.ged", "../Output")
cl.rename_file("../Output/gedcom.ged", "../Output/"+Seeder+".ged")
print("Done, your gedcom is in the Output folder")
