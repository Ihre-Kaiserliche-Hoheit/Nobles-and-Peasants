#This File only exists to test different code bits and pieces
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random
import csv

nameListM = ["Heinrich", "Reinhardt", "Adam", "Peter", "Günter", "Johan", "Hans", "Franz", "Friedrich", "Uwe", "Johannes", "Michael", "Wilhelm"]
nameListF = ["Eva", "Nina", "Johanna", "Berbel", "Lisa", "Frida", "Wilhelmina", "Svenja", "Sonja", "Marie", "Maria", "Uta", "Hildegard", "Lena"]
sexList = ["Male", "Female"]
name = ""
sex = ""
N = 5 #Starting population
total_population = [] #Total population from start to end
population = [] #Currently alive population
potential_partners = []
age = 0

#Notes to Simulation Results:
#A start population of 5 over 75 steps will have a finial population of around 3000 +/- a few hundred based on how unbalanced the start sex ratio is and if RNGesus likes you

class person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        sex = random.choice(sexList)
        if sex == "Male":
            name = random.choice(nameListM)
        elif sex == "Female":
            name = random.choice(nameListF)
        self.name = name
        #self.patronym = ""
        #self.lastname = lastname
        self.sex = sex
        self.age = age
        self.father = []
        self.father_id = ""
        self.mother = []
        self.mother_id = ""
        self.spouse = []
        self.spouse_id = ""
        self.alive = True
    def age_update(self, population, total_population):
        age = self.age
        age = age+1
        self.age = age
        #print(self.age)
        #KILL THEM ALL!
        if age >= 50: #Filters out Agents that are too young to die of old age
            if age >= 50 and age <= 60:
                if random.randint(0, 100) < 10: #This should be a 10% chance of dying
                    self.alive = False
                    population.remove(self) #Remove the agent from the alive population
                    #del population[self.unique_id] #Remove the agent from the alive population
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
    def limit_partner(self, population):
        pass
    def find_partner(self, population):
        #Chose two randos to marry
        i = random.randint(0, len(population)-1)
        j = random.randint(0, len(population)-1)
        while i == j:
            j = random.randint(0, len(population)-1)
        #print(i) #Debug Code
        #print(j) #Debug Code
        i = population[i]
        j = population[j]
        sg = 0   
        while i.sex == j.sex and sg <= 10:
            j = random.randint(0, len(population)-1)
            j = population[j]
            sg = sg+1
            #print("new partner 1") #Debug Code
        while j.spouse_id != "" and sg <= 10:
            j = random.randint(0, len(population)-1)
            j = population[j]
            sg = sg+1
            #print("new partner 2") #Debug Code
        while i.spouse_id != "" and sg <= 10:
            i = random.randint(0, len(population)-1)
            i = population[i]
            sg = sg+1
            #print("new partner 3") #Debug Code
        #A bunch of code that prevents non-reproductive partnerships
        if i.sex == j.sex:
            if i.spouse_id != "":
                j.spouse_id = ""
            elif j.spouse_id != "":
                i.spouse_id = ""
            else:
                pass
        elif i.spouse_id == i.unique_id or j.spouse_id == j.unique_id:
            if i.spouse_id == i.unique_id:
                i.spouse_id = ""
            elif j.spouse_id == j.unique_id:
                j.spouse_id = ""
        #Age restrictions! Below 16 is one big no-no
        elif i.age <= 16 or j.age <= 16:
            if i.age <= 16:
                i.spouse_id = ""
                j.spouse_id = ""
            elif j.age <= 16:
                i.spouse_id = ""
                j.spouse_id = ""
        #Sorry, but this is an milf free zone!
        elif i.age >= 50 or j.age >= 50:
            if i.age >= 50:
                i.spouse_id = ""
                j.spouse_id = ""
            elif j.age >= 50:
                i.spouse_id = ""
                j.spouse_id = ""
        else:
            i.spouse_id = j.unique_id
            j.spouse_id = i.unique_id
        sg = 0
    def have_kid(self):
        mother_id = ""
        father_id = ""
        if self.sex == "Male":
            father_id = self.unique_id
            mother_id = self.spouse_id
        elif self.sex == "Female":
            father_id = self.spouse_id
            mother_id = self.unique_id
        i = len(total_population)
        p = person(i, self)
        p.father_id = father_id #Save the id in the child for easier access
        p.mother_id = mother_id #Save the id in the child for easier access
        population.append(p)
        total_population.append(p)
        run_model.schedule.add(p)
    def step(self):
        if self.alive == True:  #Only agents that are alive should do shit, duh?
            if self.age >= 16:
                if self.spouse_id == "" or self.spouse_id == -1:
                    self.find_partner(population)
                if self.spouse_id != "":
                    self.have_kid()
            self.age_update(population, total_population)
        elif self.alive == False: #Oy, and you stay dead!
            run_model.schedule.remove(self)
        else:
            print("Oi! You got a loicens for that error!?") #Should the code, for some reason, fuck up call the bobbies over!
class WorldModel(Model):
    def __init__(self, N):
        self.num_people = N
        self.schedule = BaseScheduler(self) #RandomActivation(self)
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
for i in range(70):
    run_model.step()
    #print("\n"+"Total Population: "+str(len(population)))
#Saving and shieeeet
file.write("Unique ID; Name; Sex; Father ID; Mother ID; Spouse ID; Age; Alive"+"\n")
for i in total_population:
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.sex)+";"+str(i.father_id)+";"+str(i.mother_id)+";"+str(i.spouse_id)+";"+str(i.age)+";"+str(i.alive)+"\n")
file.close()
print("\n""The End | Total Population: "+str(len(population))) #Beatings will continue until moral and code improve!
