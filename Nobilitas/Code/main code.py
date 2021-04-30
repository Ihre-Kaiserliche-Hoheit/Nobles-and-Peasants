#TODO:
#Version 1
#   DONE -- Add namelists for men, women and lastnames
#   DONE -- Finish code for seed population
#   DONE -- Add code for marriges
#       DONE -- Find the probelm in the code 
#   DONE -- Add childbirth
#       DONE -- Add child mortality
#   DONE -- Fix any bugs that appear
#
#Version 2
#   DONE -- Add gedcom exporter
#   Add more names
#   Fix any remaining bugs
#   Fine tune systems


import random as r
import math as m
import file_code as fc
import gedcom_converter as gc


Seeder = 1223445
r.seed(Seeder) #Set seed for repeatable results

start_year = 50
year = start_year
end_year = 150

total_population = []
living_population = []
queue = []
avaible_males = []
avaible_females = []
seed = 100
k = 2000
p = seed
kr = 0 #How close the population is to k

male_names = []
female_names = []
lastnames = []

male_names = fc.txt_to_list("../Input/Male.txt")
female_names = fc.txt_to_list("../Input/Female.txt")
lastnames = fc.txt_to_list("../Input/Lastname.txt")

e = m.e

life_expecantcy_avg = 80
infant_mortality = 0.007 #In % something between 0.01 and 0.02, rec: 0.007
base_infant_mortality = infant_mortality

class person():
    def __init__(self):
        self.uid = None
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
        self.post_pregnancy_break = 0

    def update(self):
        self.age +=1
        if 18 < self.age and len(self.spouse) == 0:
            find_spouse(self)
        elif len(self.spouse) > 0 and self.sex == 1 and self.age < 40:
            rand_value = r.random()*10
            self.post_pregnancy_break -=1
            if rand_value < 6*kr:
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


def update_avaiblity_lists():
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
    List2 = []
    i = 0
    if len(List) == 0:
        return(List2)
    while len(List2) <= amount:
        thing = r.choices(List) #Note to self, don't mix up lists
        if thing not in List2:
            List2.append(thing) 
        i +=1
        if i >= amount+10: #Catch if it ends in an infinet loop because of lists that are shorter than the amount set
            return(List2)
    return(List2)


def find_spouse(searcher):
    pool_of_possible_spouses = []
    
    if searcher.sex == 0:
        pool_of_possible_spouses = create_random_list_of_uniques(avaible_females, 20)
    else:
        pool_of_possible_spouses = create_random_list_of_uniques(avaible_males, 20)

    if 0 < len(pool_of_possible_spouses):
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
    
    value = value + asses_age(other)

    return(value)


def asses_age(other):
    value = 0
    if 35 < other.age:
        value = value - 7

    elif other.age < 25:
        value += 10

    else:
        value += 2

    return(value)
          
def from_thin_air(person):
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
    person.death_date = year
    living_population.remove(person)

def set_name(person):
    if person.sex == 0:
        person.name = r.choices(male_names)

    else:
        person.name = r.choices(female_names)

def add_to_population(person):
    total_population.append(person)
    living_population.append(person)


def calc_death_chance(x): #x = age_dif
    A = x + life_expecantcy_avg
    d1 = base_infant_mortality*e**((-5*(A))*(p/k))
    d2 = (50/(1+e**(-0.19*(x+8))))/100
    d3 = (0.0004*A+0.00001)*e**(1-A/life_expecantcy_avg)
    #dc = round(base_infant_mortality**(k/p)+(50/(1+e**(-0.1*(x-50)))/100), 8) #One go version
    dc = round(d1+d2+d3, 8)
    return(dc)

for i in range(seed):
    #Create starting population
    new_person = person()
    from_thin_air(new_person)
    
   
while year < end_year:
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

fc.delete_file("raw_output.txt")
fc.move_file("gedcom.ged", "../Output")
