#This File only exists to test different code bits and pieces
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random

nameListM = ["Heinrich", "Reinhardt", "Adam", "Peter", "Günter", "Johan", "Hans", "Franz"]
nameListF = ["Eva", "Nina", "Johanna", "Berbel", "Lisa"]
sexList = ["Male", "Female"]
name = ""
sex = ""
N = 4
population = []

class person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        sex = random.choice(sexList)
        if sex == "Male":
            name = random.choice(nameListM)
        elif sex == "Female":
            name = random.choice(nameListF)
        self.name = name
        #self.patronym = patronym
        #self.lastname = lastname
        self.sex = sex
        #self.father = father
        #self.mother = mother
    def setup(self):
        pass
    def step(self):
        print("Hi, I'm "+str(self.name)+" and I'm "+str(self.sex)+" and my ID is "+str(self.unique_id))
        #Chose two randoms
        i = random.randint(0, len(population)-1)
        j = random.randint(0, len(population)-1)
        while i == j:
            j = random.randint(0, len(population)-1)
        #print(i) #Debug Code
        #print(j) #Debug Code
        i = population[i]
        j = population[j]
        while i.sex == j.sex:
            j = random.randint(0, len(population)-1)
            j = population[j]
            print("new partner") #Debug Code
        print(j.name) #Debug Code
        print(i.name) #Debug Code
class WorldModel(Model):
    def __init__(self, N):
        self.num_people = N
        self.schedule = RandomActivation(self)
        #create people
        for i in range(self.num_people):
            #sex = random.choice(sexList)
            p = person(i, self)
            population.append(p)
            self.schedule.add(p)    
    def step(self):
        self.schedule.step()

run_model = WorldModel(N)
run_model.step()
