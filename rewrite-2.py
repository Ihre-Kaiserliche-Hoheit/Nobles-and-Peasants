import numpy as np
import random
import csv
import webbrowser
from mesa_geo import GeoSpace, GeoAgent, AgentCreator
from mesa import Model

#Read Me
##Character free version
##TODO:
###Add all the Values needed

current_year = 0 #The current year
start_year = 0 #The year the sim starts
end_year = 0 #The year the sim ends
age_of_the_world = "" #Which age the world is in; List of Ages: Age of Myth, Age of Legend, Age of Heros, etc
arcane_level = 0 #How much magic exists in the world

class house():
    def __init__(self):
        super().__init__(self)
        #Base Infos
        self.self_id = ""
        self.name = ""
        #Greater Dynastic Infos
        self.child_houses = [] #List of all DIRECT cadet branches
        self.parent_house = [] #Parent house
        self.parent_house_name = "" #For easy access
        #Status Infos
        self.founding_year = "" #When the house was founded
        self.extiction_year = "" #When the house went extinct
        self.extinct = False #If the house is extinct or not
class title():
    def __init__(self):
        super().__init__(self)
        self.tier = "" #Which tier the Title is; Duchy for example
        self.prefix = "" #How the owner is called; Duke for example
        self.settelments = [] #Settelments that are ruled by the title
        self.owner = "" #Who holds the title
        self.owner_house = []
        self.vassals = [] #Who the title rules over
        self.liege = [] #Which title's subject it is; can never be of an higher tier then the liege
class settelment():
    def __init__(self):
        super().__init__(self)
        self.position = [] #The position on the map in form of corrdinats
        self.land = 0 #How much land belongs to the settelment
        self.population = 0 #Total of all end_size from the population list
        self.kind = "" #Is it a village, town, city or something entirly different?
        self.liege = [] #Which title the settelment belongs to
class pop():
    def __init__(self):
        super().__init__(self)
        self.job = "" #What job they work in
        self.beliefs = "" #What the pops beliefs is important to them
        self.culture = ""
        self.religion = ""
        self.race = "" #Human, Orc or Half-Orc
        self.wealth = 0 #How much money they have
        self.base_size = 0 #How large the pop is without any modifiers
        self.scale = 0 #The scale of the pop; something between 0.01 and 5
        self.end_size = 0 #How large the pop is after adding all modifiers to it
        self.home = [] #In which settelment they live
class core(): #Here comes all the action
    def __init__(self):
        pass
    def step():
        pass
