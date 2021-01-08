import numpy as np
import random as r
import csv
import webbrowser
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.space import MultiGrid
import networkx as nx
import matplotlib.pyplot as plt
#Read Me
##TODO:
###Add all the Values needed

total_population = [] #List of all people to have ever lived
living_population = []
valid_spouses = []
valid_spouse = []
current_year = 0 #The current year
start_year = 100 #The year the sim starts
end_year = 500 #The year the sim ends
age_of_the_world = "" #Which age the world is in; List of Ages: Age of Myth, Age of Legend, Age of Heros, etc
starting_population = 20
sexes = ["Male", "Female"]
debug_mode = False
#Coded inputs

#Setup
print("Starts...")
print("Load names...")
HumanM = open("HumanMaleNames.txt", "r", newline="")
HumanF = open("HumanFemaleNames.txt", "r", newline="")
HumanL = open("HumanLastNames.txt", "r", newline="")
MaleNames = HumanM.read().splitlines()
FemaleNames = HumanF.read().splitlines()
Lastnames = HumanL.read().splitlines()
HumanL.close()
HumanF.close()
HumanM.close()

def debug(debug_message):
    if debug_mode == True:
        print(debug_message)

class character(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #Base Infos
        #self.unique_id = unique_id #The Unique ID
        self.name = "" #The Name
        self.patronym = ""
        self.lastname = ""
        self.sex = "" #Male or Female
        self.age = 0 #What age the Character is
        self.health = 0 #Health, influences how old a Character can get
        #Family Infos; Infos about the Characters family
        self.father = [] #The Father
        self.father_id = "" #For easy access
        self.mother = [] #The Mother
        self.mother_id = "" #For easy access
        self.spouse = [] #The Spouse
        self.spouse_id = "" #For easy access
        self.children = [] #List of all their children
        self.preg_recov_counter = 0 #How long until the character can have kids again, if they are female
        #Location Infos; Where the Character is
        #Genetic Infos; Infos about the genes of the Character
        self.arcanlevel = 0 #16; 14; 10; 8; 7; 4; 2 
        self.magi = "" #God; Lesser God; Angle; Demi-God; Godtouched; Pureblood; Mundane
        #Status Infos; Infos about the Characters birth and death
        self.birth_d = "" #The birth year
        self.death_d = "" #The death year
        self.alive = True #If the Character is alive
        #Property Infos; What the Character owns
        self.land = 0 #How much land the Character owns
        #Other Infos; Everything that doesn't fit in the above
        self.rank = "" #The rank the Character has in society; Possible ranks are: Freeman/Freewoman, Burgher, Patrician, Minor Noble, Greater Noble, Royal; Based on the amount of land they have
        self.traits = []
        
    def pregnacy(self):
        debug("debug_pregnacy_1")
        if self.preg_recov_counter <= 0:
            debug("debug_pregnacy_2")
            rn = r.randint(0, 10)
            rn = rn+self.arcanelevel
            if rn >= 17:
                self.preg_recov_count = 10
            elif rn >= 12:
                self.preg_recov_count = 7
            else:
                debug("debug_pregnacy_3")
                mother = self
                mother.birth(mother)
        else:
            self.preg_recov_counter = self.preg_recov_counter-1
            rn = r.randint(0, 100)
            if rn <= 20:
                mother.preg_recov_count = 3
            elif rn <= 40:
                mother.preg_recov_count = 4
            elif rn <= 60:
                mother.preg_recov_count = 5
            elif rn <= 80:
                mother.preg_recov_count = 4
            else:
                mother.preg_recov_count = 2
                
    def birth(self, mother):
        debug("debug_birth_1")
        mother_id = mother.unique_id
        father = mother.spouse[0]
        father_id = mother.spouse_id
        C = len(total_population)+1
        child = character(C, Model)
        #child.unique_id = 
        child.father_id = father_id
        child.father = father
        child.mother_id = mother_id
        child.mother = mother
        child.sex = r.choice(sexes)
        child.arcanelevel = int((father.arcanelevel+mother.arcanelevel)/2-r.randint(0,2)) #Gives the median value of parents arcanelevel; Always rounds down
        child.divinity(child)
        child.health = (r.randint(1, 4)+child.arcanelevel)
        child.get_firstname(child)
        if father.lastname == "":
            if child.sex == "Male":
                child.patronym = str(father.name)+"ssohn"
            elif child.sex == "Female":
                child.patronym = str(father.name)+"stochter"
        else:
            child.lastname = father.lastname
        child.birth_d= current_year
        mother.children.append(child)
        father.children.append(child)
        total_population.append(child)
        living_population.append(child)
        simulation.schedule.add(child)

    def divinity(self, child):
        target = child
        if target.arcanelevel <= 2:
            target.magi = "Mundane"
        elif target.arcanelevel <= 4:
            target.magi = "Pureblood"
        elif target.arcanelevel <= 7:
            target.magi = "Godtouched"
        elif target.arcanelevel <= 8:
            target.magi = "Demi-God"
        elif target.arcanelevel <= 10:
            target.magi = "Angle"
        elif target.arcanelevel <= 14:
            target.magi = "Lesser God"
        elif target.arcanelevel <= 16:
            target.magi = "God" 
        else:
            target.arcanelevel = 1
            target.magi = "Mundane"
            
    def get_firstname(self, target):
        named = target
        if named.sex == "Male":
            named.name = r.choice(MaleNames)
        else:
            named.name = r.choice(FemaleNames)
            
    def get_lastname(self):
        father = self.father
        if current_year >= start_year+250:
            if father.lastname != "" and self.lastname == "":
               self.lastname = father.lastname
            else:
                rn = r.randint(0,1)
                if rn == 0:
                    self.lastname = r.choice(Lastnames)
                else:
                    self.lastname = self.patronym

    def find_spouse(self):
        valid_spouse = []
        #vpr = len(valid_spouses)
        spouse_choice = r.choices(valid_spouses, k=200)
        vpr = len(spouse_choice)
        for i in range(vpr):
            target = spouse_choice[i]
            if ((target != self) and
                ((target.father_id != self.father_id) or (target.father_id == "" and self.father_id == "")) and
                (target.sex != self.sex) and
                ((target.age <= 45 and target.age >= 16) or (target.age >= 16 and (target.magi == "God" or target.magi == "Lesser God" or target.magi == "Angel" or target.magi == "Demi-God"))) and
                (target.spouse_id == "")
                ):
            #########################################
                valid_spouse.append(target)
            else:
                pass
        if len(valid_spouse) >= 1:
            target = r.choice(valid_spouse)
            #And now kiss
            self.spouse.append(target)
            target.spouse.append(self)
            target.spouse_id = self.unique_id
            self.spouse_id = target.unique_id

    def age_update(self):
        self.age = self.age+1
        if self.age < 20:
            self.health = self.health+1
        elif self.age > 25:
            self.health = self.health-0.5
        else:
            pass
        if self.age >= 45 and not (self.magi == "God" or self.magi == "Lesser God"):
            ind = valid_spouses.index(self)
            if valid_spouses.index(self) == True:
                valid_spouses.remove(self)
        else:
            valid_spouses.append(self)
        if self.health <= 0:
           self.death(self)

    def death(self, dyee):
        dyee.alive = False
        living_population.remove(dyee)
        dyee.death_d = current_year
        simulation.schedule.remove(dyee)
        
    def step(self):
        if self.alive == True: #Safe guard
            self.age_update()
            self.get_lastname
            if self.spouse_id == "":
                self.find_spouse()
            else:
                pass
            if self.sex == "Female" and self.spouse_id != "":
                spouse = self.spouse[0]
                if spouse.alive == True:
                    self.pregnacy()
        
class core(Model): #Here comes all the action
    def __init__(self): 
        self.setup_population(starting_population)
        
    def setup_population(self, starting_population):
        self.schedule = RandomActivation(self)
        debug("debug_setup")
        for i in range(starting_population):
            p = character(i, self)
            p.age = 20
            p.birth_d = start_year-p.age
            p.sex = r.choice(sexes)
            p.arcanelevel = r.randint(10, 16)
            p.health = r.randint(4, 9)+p.arcanelevel+5
            p.divinity(p)
            p.get_firstname(p)
            living_population.append(p)
            total_population.append(p)
            valid_spouses.append(p)
            self.schedule.add(p)

    def big_dead(self, deaths): #Event to cull big populations, cuz fuck em
        #This thing only exist because the populations grew to big and slowed the programm down too much.
        #Now the population will stay somewhere around 2300 people.
        soon_ded = r.choices(living_population, k=deaths)
        for i in range(len(soon_ded)):
            sd = soon_ded[i]
            if sd.alive == True:
                sd.death(sd)
                     
    def step(self):
        self.schedule.step()
        

current_year = start_year
debug("debug_start")
simulation = core() #Don't change
starting_population = 0
print("Start generation...")
for year in range(start_year, end_year):
    simulation.step()
    if len(living_population) >= 2000:
            d = int(round(len(living_population)/4, 0))
            simulation.big_dead(d)
    current_year = current_year+1
    if current_year % 10 == 0:
        print("Year: "+str(current_year)+" "+str(len(living_population)))
print("Finished generation...")
print(len(total_population))
file = open("save_file_2.csv", "w", newline="")
file.write("Unique ID; Name; Patronym; Lastname; Sex; Father ID; Mother ID; Spouse ID; Birth; Death; Age"+"\n")
living = 0
for j in range(len(total_population)):
    i = total_population[j]
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.patronym)+";"+str(i.lastname)+";"+str(i.sex)+";"+str(i.father_id)+";"+str(i.mother_id)+";"+str(i.spouse_id)+";"+str(i.birth_d)+";"+str(i.death_d)+";"+str(i.age)+";"+str(i.magi)+"\n")
print("\n""The End | Total Population: "+str(len(living_population))) #Beatings will continue until moral and code improve!
file.close()
