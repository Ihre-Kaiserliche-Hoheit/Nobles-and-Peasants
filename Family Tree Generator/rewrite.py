import numpy as np
import random as r
import csv
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler

total_population = [] #List of all people to have ever lived
living_population = []
valid_spouses = []
valid_spouse = []
current_year = 0 #The current year
start_year = 100 #The year the sim starts
end_year = 400 #The year the sim ends
starting_population = 20
sexes = ["Male", "Female"]

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

class character(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #Base Infos
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
        #Status Infos; Infos about the Characters birth and death
        self.birth_d = "" #The birth year
        self.death_d = "" #The death year
        self.alive = True #If the Character is alive
        
    def pregnacy(self):
        if self.preg_recov_counter <= 0:
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
        mother_id = mother.unique_id
        father = mother.spouse[0]
        father_id = mother.spouse_id
        C = len(total_population)+1
        child = character(C, Model)
        child.father_id = father_id
        child.father = father
        child.mother_id = mother_id
        child.mother = mother
        child.sex = r.choice(sexes)
        child.health = (r.randint(2, 4))
        child.get_firstname(child)
        if father.lastname == "":
            if child.sex == "Male":
                child.patronym = str(father.name)+"ssohn"
            elif child.sex == "Female":
                child.patronym = str(father.name)+"stochter"
            child.get_lastname
        else:
            child.lastname = father.lastname
        child.birth_d= current_year
        mother.children.append(child)
        father.children.append(child)
        total_population.append(child)
        living_population.append(child)
        simulation.schedule.add(child)

    def get_firstname(self, target):
        named = target
        if named.sex == "Male":
            named.name = r.choice(MaleNames)
        else:
            named.name = r.choice(FemaleNames)
            
    def get_lastname(self):
        father = self.father
        if current_year > (start_year+200):
            if self.lastname == "":
                rn = r.randint(0,1)
                if rn == 0:
                    self.lastname = r.choice(Lastnames)
                else:
                    self.lastname = self.patronym

    def find_spouse(self):
        valid_spouse = []
        spouse_choice = r.choices(valid_spouses, k=200)
        vpr = len(spouse_choice)
        for i in range(vpr):
            target = spouse_choice[i]
            if ((target != self) and
                ((target.father_id != self.father_id) or (target.father_id == "" and self.father_id == "")) and
                (target.sex != self.sex) and
                (target.age <= 45 and target.age >= 16) and
                (target.spouse_id == "")
                ):
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
        if self.age >= 45:
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
            self.get_lastname() #Why the fuck didn't I add brackets here? Now it should work
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
        for i in range(starting_population):
            p = character(i, self)
            p.age = 20
            p.birth_d = start_year-p.age
            p.sex = r.choice(sexes)
            p.health = r.randint(4, 8)
            p.get_firstname(p)
            living_population.append(p)
            total_population.append(p)
            valid_spouses.append(p)
            self.schedule.add(p)

    def big_dead(self, deaths): #Event to cull big populations, cuz fuck em
        #This thing only exist because the populations grew to big and slowed the programm down too much.
        #Now the population will stay somewhere below 2500 people.
        soon_ded = r.choices(living_population, k=deaths)
        for i in range(len(soon_ded)):
            sd = soon_ded[i]
            if sd.alive == True:
                sd.death(sd)
                     
    def step(self):
        self.schedule.step()

current_year = start_year
simulation = core() #Don't change
starting_population = 0
print("Start generation...")
for year in range(start_year, end_year):
    simulation.step()
    if len(living_population) >= 1500:
            d = int(round(len(living_population)/2, 0))
            simulation.big_dead(d)
    current_year = current_year+1
    if current_year % 10 == 0:
        print("Year: "+str(current_year)+" "+str(len(living_population)))
print("\n""The End | Total Population: "+str(len(living_population)))
print("Finished generation...")
file = open("save_file.csv", "w+", newline="")
file.write("Unique ID; Name; Patronym; Lastname; Sex; Father ID; Mother ID; Spouse ID; Birth; Death; Age"+"\n")
for j in range(len(total_population)):
    i = total_population[j]
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.patronym)+";"+str(i.lastname)+";"+str(i.sex)+";"+str(i.father_id)+";"+str(i.mother_id)+";"+str(i.spouse_id)+";"+str(i.birth_d)+";"+str(i.death_d)+";"+str(i.age)+"\n")
file.close()
print("End of Program")
