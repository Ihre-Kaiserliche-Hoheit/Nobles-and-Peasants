#This File only exists to test different code bits and pieces
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random
import csv
import webbrowser

#Names for Men
nameListM = ["Heinrich", "Reinhardt", "Adam", "Peter", "Günter", "Johan", "Hans", "Franz",
             "Friedrich", "Uwe", "Johannes", "Michael", "Wilhelm", "Erik", "Klaus"]
#Names for Women
nameListF = ["Eva", "Nina", "Johanna", "Berbel", "Lisa", "Frida", "Wilhelmina",
             "Svenja", "Sonja", "Marie", "Maria", "Uta", "Hildegard", "Lena", "Erika"]
#Lastnames/Surenames for People
nameListL = []
sexList = ["Male", "Female"]
#name = ""
sex = ""
N = 5 #Starting population
total_population = [] #Total population from start to end
population = [] #Currently alive population
valid_partner = [] #Valid Partners; Meta value
age = 0

#Notes:
#A start population of 5 over 75 steps will have a finial population of around 300+/-100 based on how unbalanced the start sex ratio is and if RNGesus likes you
#!!!!!NEVER insert 0 as generic relation ANYWHERE!!!!!

class person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        sex = random.choice(sexList)
        if sex == "Male":
            name = random.choice(nameListM)
        elif sex == "Female":
            name = random.choice(nameListF)
        self.name = name
        self.patronym = ""
        self.lastname = ""
        self.sex = sex
        self.age = age
        self.father = []
        self.father_id = ""
        self.mother = []
        self.mother_id = ""
        self.spouse = []
        self.spouse_id = ""
        self.alive = True
        #self.pregnant = False
        #self.preg_count = 0
        self.preg_recov_count = 0
    def age_update(self, population, total_population):
        age = self.age
        age = age+1
        self.age = age
        #KILL THEM ALL!
        if age >= 50: #Filters out Agents that are too young to die of old age
            if age >= 50 and age <= 60:
                if random.randint(0, 100) < 10: #This should be a 10% chance of dying
                    self.alive = False
                    population.remove(self) #Remove the agent from the alive population
                    run_model.schedule.remove(self)
            elif age >= 61 and age <= 70:
                if random.randint(0, 100) < 30: #This should be a 30% chance of dying
                    self.alive = False
                    population.remove(self) #Remove the agent from the alive population
                    run_model.schedule.remove(self)
            elif age >= 71:
                if random.randint(0, 100) < 50: #This should be a 50% chance of dying
                    self.alive = False
                    population.remove(self) #Remove the agent from the alive population
                    run_model.schedule.remove(self)
    def find_partner(self, population):
        #pre-select partners
        valid_partner.append(0)
        valid_partner.clear()
        #ps_target: Pre-Select Target
        for ps_target in range(len(population)-1):
            #in the end add all valid people to valid_partner
            ps_target = population[ps_target]
            if ps_target.spouse_id != "":
                pass
            else:
                if self == ps_target:
                    pass
                elif self != ps_target:
                    if self.sex == ps_target.sex:
                        pass
                    elif self.sex != ps_target.sex:
                        if self.spouse_id != "":
                            pass
                        else:
                            #No Incest
                            if (ps_target.father_id == "" and self.father_id == "") or (ps_target.mother_id == "" and self.mother_id == ""):
                                valid_partner.append(ps_target)
                            else:
                                if ps_target.father_id == self.father_id or ps_target.mother_id == self.mother_id:
                                    pass
                                else:
                                    valid_partner.append(ps_target)
        #chose random person from the valid partner list
        #s_target: Select Target
        if len(valid_partner) > 0:
            s_target = random.randint(0, len(valid_partner)-1)
            while self == s_target:
                s_target = random.randint(0, len(valid_partner)-1)
            s_target = valid_partner[s_target]
            sg = 0   
            while self.sex == s_target.sex and sg <= 10:
                s_target = random.randint(0, len(valid_partner)-1)
                s_target = valid_partner[s_target]
                sg = sg+1
                #print("new partner 1") #Debug Code
            while s_target.spouse_id != "" and sg <= 10:
                s_target = random.randint(0, len(valid_partner)-1)
                s_target = valid_partner[s_target]
                sg = sg+1
                #print("new partner 2") #Debug Code
                
            #Post-selection to make sure everything is okay
            if self.sex == s_target.sex:
                if self.spouse_id != "":
                    s_target.spouse_id = ""
                elif s_target.spouse_id != "":
                    self.spouse_id = ""
                else:
                    pass
            elif self.spouse_id == self.unique_id or s_target.spouse_id == s_target.unique_id:
                if self.spouse_id == self.unique_id:
                    self.spouse_id = ""
                elif s_target.spouse_id == s_target.unique_id:
                    s_target.spouse_id = ""
            #Age restrictions! Below 16 is one big no-no
            elif self.age <= 16 or s_target.age <= 16:
                if self.age <= 16:
                    self.spouse_id = ""
                    s_target.spouse_id = ""
                elif s_target.age <= 16:
                    self.spouse_id = ""
                    s_target.spouse_id = ""
            #Sorry, but this is an milf free zone!
            elif self.age >= 45 or s_target.age >= 45:
                if self.age >= 45:
                    self.spouse_id = ""
                    s_target.spouse_id = ""
                elif s_target.age >= 45:
                    self.spouse_id = ""
                    s_target.spouse_id = ""
            else:
                self.spouse_id = s_target.unique_id
                self.spouse.append(s_target)
                s_target.spouse_id = self.unique_id
                s_target.spouse.append(self)
        sg = 0
    def have_kid(self):
        if self.sex == "Female":
            mother = self
            mother_id = self.unique_id
            father = self.spouse[0]
            father_id = self.spouse_id
        elif self.sex == "Male":
            mother = self.spouse[0]
            mother_id = self.spouse_id
            father = self
            father_id = self.unique_id
        if mother.preg_recov_count == 0:
            i = len(total_population) #total_population, not population! If you use population you will get multiple agents with the same ID
            child = person(i, self)
            child.father_id = father_id #Save the id in the child for easier access
            child.father = father #Save link to father for easy access
            child.mother_id = mother_id #Save the id in the child for easier access
            child.mother = mother #Save link to mother for easy access
            if child.sex == "Male":
                child.patronym = str(father.name)+"ssohn"
            elif child.sex == "Female":
                child.patronym = str(father.name)+"stochter"
            mother.preg_recov_count = 2
            population.append(child)
            total_population.append(child)
            run_model.schedule.add(child)
        elif mother.preg_recov_count >= 1:
            mother.preg_recov_count = mother.preg_recov_count-1
    def step(self):
        if self.alive == True:  #Only agents that are alive should do shit, duh?
            if self.age >= 16:
                if self.spouse_id == "" or self.spouse_id == -1:
                    self.find_partner(population)
                if self.spouse_id != "" and self.sex == "Female":
                    self.have_kid()
            self.age_update(population, total_population)
        elif self.alive == False: #Oy, and you stay dead!
            run_model.schedule.remove(self)
        else:
            print("Oi! You got a loicens for that error!?") #Should the code, for some reason, fuck up call the bobbies over!
            webbrowser.open("https://www.youtube.com/watch?v=G1IbRujko-A", new=2) #Just incase someone isn't paying tax... I mean attention!
class WorldModel(Model):
    def __init__(self, N):
        self.num_people = N
        self.schedule = RandomActivation(self) #BaseScheduler(self) 
        #create people
        for i in range(self.num_people):
            #Some basic shit to set up the starting population
            p = person(i, self)
            p.age = 20
            population.append(p)
            total_population.append(p)
            self.schedule.add(p)
    def step(self):
        self.schedule.step()
run_model = WorldModel(N)
file = open("save_file_2.csv", "w", newline="")
for i in range(75):
    run_model.step()
    print("\n"+"Total Population: "+str(len(population)))
#Saving and shieeeet
file.write("Unique ID; Name; Patronym; Sex; Father ID; Mother ID; Spouse ID; Age; Alive"+"\n")
for i in total_population:
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.patronym)+";"+str(i.sex)+";"+str(i.father_id)+";"+str(i.mother_id)+";"+str(i.spouse_id)+";"+str(i.age)+";"+str(i.alive)+"\n")
file.close()
print("\n""The End | Total Population: "+str(len(population))) #Beatings will continue until moral and code improve!
