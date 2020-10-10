from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random
import csv

class pop(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
            self.settelment = []
            self.religion = ""
            self.culture = ""
            self.wealth = ""
            self.job = ""
    def step(self):
        pass

class settelment(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = ""
        #self.leader = []
        self.population = []
        self.pops = []
        self.pop_k = 100
        self.pos = [0,0]
    def step(self):
        pass

class Model(Model):
    def __init__(self):
        pass
    def step(self):
        pass

run_model = Model()
