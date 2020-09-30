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
N = 5
population = []
potential_partners = []
#father = []
#father_id = ""
#mother = []
#mother_id = ""
#alive = True
age = 0

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
    def age_update(self):
        age = self.age
        age = age+1
        self.age = age
        #print(self.age)
        if age >= 50:
            if age >= 50 and age <= 60:
                if random.randint(0, 100) < 10:
                    self.alive = False
                    run_model.schedule.remove(self)
            elif age >= 61 and age <= 70:
                if random.randint(0, 100) < 30:
                    self.alive = False
                    run_model.schedule.remove(self)
            elif age >= 71:
                if random.randint(0, 100) < 50:
                    self.alive = False
                    run_model.schedule.remove(self)
    def limit_partner(self, population):
        pass
    def find_partner(self, population):
        #Chose two randoms
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
        #if j.spouse_id == i.unique_id and i.spouse_id == j.unique_id:
            #print(str(i.unique_id)+" is married to "+str(j.unique_id))
            #pass
        #else:
            #pass
    def have_kid(self):
        mother_id = ""
        father_id = ""
        if self.sex == "Male":
            father_id = self.unique_id
            mother_id = self.spouse_id
        elif self.sex == "Female":
            father_id = self.spouse_id
            mother_id = self.unique_id
        i = len(population)
        p = person(i, self)
        p.father_id = father_id
        p.mother_id = mother_id
        population.append(p)
        #print(str(p.unique_id)+" was born to "+str(father)+" and "+str(mother))
        run_model.schedule.add(p)
    def step(self):
        if self.alive == True:
            if self.age >= 16:
                if self.spouse_id == "" or self.spouse_id == -1:
                    self.find_partner(population)
                if self.spouse_id != "":
                    self.have_kid()
            self.age_update()
        elif self.alive == False:
            run_model.schedule.remove(self)
        else:
            print("Oy mate, something isn't right!")
class WorldModel(Model):
    def __init__(self, N):
        self.num_people = N
        self.schedule = BaseScheduler(self) #RandomActivation(self)
        #create people
        for i in range(self.num_people):
            #sex = random.choice(sexList)
            p = person(i, self)
            p.age = 20
            population.append(p)
            self.schedule.add(p)
    def step(self):
        self.schedule.step()
run_model = WorldModel(N)
file = open("save_file_2.csv", "w", newline="")
for i in range(50):
    run_model.step()
    #print("\n"+"Total Population: "+str(len(population)))
file.write("Unique ID; Name; Sex; Father ID; Mother ID; Spouse ID"+"\n")
for i in population:
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.sex)+";"+str(i.father_id)+";"+str(i.mother_id)+";"+str(i.spouse_id)+"\n")
file.close()
print("\n""The End | Total Population: "+str(len(population)))
