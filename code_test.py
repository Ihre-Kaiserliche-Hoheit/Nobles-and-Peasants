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
nameListF = ["Eva", "Nina", "Johanna", "Berbel", "Lisa", "Frida", "Wilhelmina", "Svenja", "Sonja", "Marie", "Maria", "Uta", "Hildegard"]
sexList = ["Male", "Female"]
name = ""
sex = ""
N = 5
population = []
father = ""
mother = ""
alive = True
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
        #self.lastname = lastname
        self.sex = sex
        self.age = age
        self.father = father
        self.mother = mother
        self.spouse = ""
        self.alive = alive
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
        while j.spouse != "" and sg <= 10:
            j = random.randint(0, len(population)-1)
            j = population[j]
            sg = sg+1
            #print("new partner 2") #Debug Code
        while i.spouse != "" and sg <= 10:
            i = random.randint(0, len(population)-1)
            i = population[i]
            sg = sg+1
            #print("new partner 3") #Debug Code
        if i.sex == j.sex and sg >= 10:
            if i.spouse != "":
                j.spouse = ""
            elif j.spouse != "":
                i.spouse = ""
            else:
                pass
        else:
            i.spouse = j.unique_id
            j.spouse = i.unique_id
        sg = 0
        if j.spouse == i.unique_id and i.spouse == j.unique_id:
            #print(str(i.unique_id)+" is married to "+str(j.unique_id))
            pass
        else:
            pass
    def have_kid(self):
        mother = ""
        father = ""
        if self.sex == "Male":
            father = self.unique_id
            mother = self.spouse
        elif self.sex == "Female":
            father = self.spouse
            mother = self.unique_id
        i = len(population)
        p = person(i, self)
        p.father = father
        p.mother = mother
        population.append(p)
        #print(str(p.unique_id)+" was born to "+str(father)+" and "+str(mother))
        run_model.schedule.add(p)
    def step(self):
        if self.alive == True:
            if self.age >= 16:
                if self.spouse == "" or self.spouse == -1:
                    self.find_partner(population)
                if self.spouse != "":
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
    #print("")
for i in population:
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.sex)+";"+str(i.father)+";"+str(i.mother)+";"+str(i.spouse)+"\n")
file.close()
print("\n""The End | Total Population: "+str(len(population)))
