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

class person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        sex = random.choice(sexList)
        if sex == "Male":
            name = random.choice(nameListM)
        elif sex == "Female":
            name = random.choice(nameListF)
        self.name = name
        self.sex = sex
    def step(self):
        print("Hi, I'm "+str(self.name)+" and I'm "+str(self.sex)+" and my ID is "+str(self.unique_id))

class WorldModel(Model):
    def __init__(self, N):
        self.num_people = N
        self.schedule = RandomActivation(self)
        #create people
        for i in range(self.num_people):
            #sex = random.choice(sexList)
            p = person(i, self)
            self.schedule.add(p)
    def step(self):
        self.schedule.step()

run_model = WorldModel(5)
run_model.step()
