#TODO:
#   Fix any remaining bugs
#   Fine tune systems


#NOTE:
#I likely don't know either how half of this works in a few weeks - Kaiser

import random as r
import math as m
import file_code as fc
import gedcom_converter as gc
import shutil
from datetime import datetime as d


#Values to tweak and stuff
#If not changed the Seed of the randomness will be the current date
time = d.now()
Seeder = str(time.strftime("%H:%M:%S %d.%m.%Y")) #Seed for the randomness of the simulation, change this every run!
print(Seeder)
r.seed(Seeder) #Set seed for repeatable results

#Change values to the setting ones
settings = fc.txt_to_list("../Input/Settings.txt")
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

total_population = [] #List of EVERY person that ever lived
living_population = [] #List of living people
queue = [] #Acting queue for characters
avaible_males = [] #List of fertil and unmarried men
avaible_females = [] #List of fertil and unmarried women

p = seed #current population count
kr = 0 #How close the population is to k
base_infant_mortality = infant_mortality #Base infant mortality, don't change directly or you may fuck stuff up

male_names = []
female_names = []
lastnames = []

male_names = fc.txt_to_list("../Input/Male.txt")
female_names = fc.txt_to_list("../Input/Female.txt")
lastnames = fc.txt_to_list("../Input/Lastname.txt")

e = m.e #Eulers number


#Person class
class person():
    def __init__(self):
        self.uid = None #The id of a character
        self.name = ""
        self.surname = ""
        self.sex = None  #0 = Man, 1 = Woman
        self.birth_date = None
        self.age = 0
        self.death_date = None

        self.father = []
        self.mother = []
        self.spouse = []
        self.children = []
        self.post_pregnancy_break = 0 #How long until a woman can have kids again

    def update(self):
        self.age +=1
        if 18 < self.age and len(self.spouse) == 0:
            find_spouse(self)
        elif len(self.spouse) > 0 and self.sex == 1 and self.age < 40:
            rand_value = r.random()*growth_influence_1
            self.post_pregnancy_break -=1
            if rand_value < preg_tweak*kr:
                self.have_kid(self, self.spouse[0])
        
        
        self.death() #Looks if they die today

    def birth(self, mother, father):
        #Create child
        child = person()
        child.uid = len(total_population)
        
        #Add parent-child relations
        child.mother.append(mother)
        mother.children.append(child)
        child.father.append(father)
        father.children.append(child)

        #Set values
        child.birth_date = year
        add_to_population(child)
        child.sex = r.randint(0, 1)
        set_name(child)
        child.surname = father.surname
        mother.post_pregnancy_break = r.randint(1, 3)

    def have_kid(self, mother, father):
        if mother.post_pregnancy_break <= 0:
            mother.birth(mother, father)
        pass

    def death(self):
        age_dif = self.age - life_expecantcy_avg #Gets how far above/below they are
        death_chance = calc_death_chance(age_dif)
        #if the value is below death_chance they die
        death_roll = round(r.random(), 8)
        if death_roll <= death_chance:
            #You died, and now get gud
            death(self)


#All the other stuff
def update_avaiblity_lists():
    #Goes through the lists for avaible men and women, may be improved for better performance
    for i in range(len(living_population)):
        person = living_population[i]
        if len(person.spouse) == 0 and (person not in avaible_males and person not in avaible_females) and person.age < 40:
            if person.sex == 0:
                avaible_males.append(person)
            elif person.sex == 1:
                avaible_females.append(person)
        elif (0 < len(person.spouse) or 40 < person.age) and (person in avaible_males or person in avaible_females):
            if (50 < person.age or 0 < len(person.spouse)) and person.sex == 0:
                avaible_males.remove(person)

            elif (40 < person.age or 0 < len(person.spouse)) and person.sex == 1:
                avaible_females.remove(person)
    remove_dead(avaible_males)
    remove_dead(avaible_females)

def remove_dead(List:list):
    try:
        for i in range(len(List)):
            person = List[i]
            if person not in living_population:
                List.remove(person)
    except IndexError:
        pass #Can be ignored? Could produce bugs, or maybe not

def create_random_list_of_uniques(List:list, amount:int):
    #Cuz I don't give a fuck if that is already possible with the random lib
    List2 = []
    i = 0
    if len(List) == 0:
        return(List2)
    while len(List2) <= amount:
        thing = r.choices(List) #Note to self, don't mix up lists
        if thing not in List2:
            List2.append(thing) 
        i +=1
        if i >= amount+10: #Catch if it ends in an infinit loop because of lists that are shorter than the amount set
            return(List2)
    return(List2)

def find_spouse(searcher):
    pool_of_possible_spouses = []
    
    #Creates a ~hopefully~ fully unqiue list of people
    if searcher.sex == 0:
        pool_of_possible_spouses = create_random_list_of_uniques(avaible_females, 20)
    else:
        pool_of_possible_spouses = create_random_list_of_uniques(avaible_males, 20)

    if 0 < len(pool_of_possible_spouses):
        #Searches for the best fit among the random people chosen
        best_fit = [""]
        best_value = -1
        for i in range(len(pool_of_possible_spouses)):
            other = pool_of_possible_spouses[i]
            other = other[0] #Is needed because for some fucking reason the above gives other as a list
            value = assigne_spouse_value(searcher, other)
            if best_value < value:
                best_fit.clear()
                best_fit.append(other)
                best_value = value
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
        value = value - 7

    elif other.age < 25:
        value += 10

    else:
        value += 2

    return(value)

def asses_relation(point1, point2):
    #Most people don't want to marry their siblings...
    value = 0
    check = False

    try:
        f1 = point1.father[0]
        f2 = point2.father[0]
        m1 = point1.mother[0]
        m2 = point2.mother[0]
        check = True

    except IndexError:
        # ... and people tend to prefer unreleated people...
        value +=5
        return(value)

    if f1 == f2 or m1 == m2:
        #... except in rare cases where everyone else is worse.
        value = -50
        
    #Maybe add more complex system for more distant relatives
    return(value)
    
def from_thin_air(person):
    #For the set up only
    #Create child
    person.uid = len(total_population)

    #Set values
    person.birth_date = year-20
    person.age = 20
    add_to_population(person)
    person.sex = r.randint(0, 1)
    set_name(person)
    person.surname = r.choices(lastnames)
    #Seed population code goes here

def death(person):
    #U ded
    person.death_date = year
    living_population.remove(person)

def set_name(person):
    if person.sex == 0:
        person.name = r.choices(male_names)

    else:
        person.name = r.choices(female_names)
    #Maybe adda list of gender-neutral names for the case this code fucks up? - Kaiser
    #Nah, this is fine - Steve

def add_to_population(person):
    #Add to both lists, cuz it is easy to have one function that does both for me
    total_population.append(person)
    living_population.append(person)

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
       
while year < end_year:
    #Simulation cycle after the creation
    year +=1
    queue = living_population
    r.shuffle(queue)
    p = len(living_population)
    try:
        kr = round(1-(p/k), 8)
    except ZeroDivisionError:
        pass
    print("Year " + str(year))
    print(len(living_population))
    update_avaiblity_lists()
    ii = 0
    while ii < len(living_population):
        c = living_population[ii]
        c.update()
        ii +=1

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
    file.write(str(person.uid) + ";" + str(person.name[0])  + ";" + str(person.surname[0])  + ";" + str(person.sex) + ";" + str(father_id)  + ";" + str(mother_id) + ";" + str(spouse_id) + ";" + str(id_list) + ";" + str(person.birth_date) + ";" + str(person.death_date) + ";" + str(person.age) + "; \n")

file.close()
gc.converter()

#Clean up, delets raw_output and moves the gedcom to the output folder
fc.delete_file("raw_output.txt")
try:
    #If this is new
    fc.move_file("gedcom.ged", "../Output")

except shutil.Error:
    #Only reason shutil is importet at all
    #Also renames the old gedcom in output to the current date
    fc.rename_file("../Output/gedcom.ged", "../Output/"+Seeder+".ged")
    fc.move_file("gedcom.ged", "../Output")
