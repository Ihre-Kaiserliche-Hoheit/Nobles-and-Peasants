
import numpy as np
import random as r
import csv
import webbrowser
from mesa import Model
import networkx as nx
import matplotlib.pyplot as plt
import pygame as pyg
#Read Me
##TODO:
###Add all the Values needed

total_population = [] #List of all people to hace ever lived
living_population = []
current_year = 0 #The current year
start_year = 0 #The year the sim starts
end_year = 0 #The year the sim ends
age_of_the_world = "" #Which age the world is in; List of Ages: Age of Myth, Age of Legend, Age of Heros, etc

#Coded inputs

#Setup
def start_exe():
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
    def __init__(self):
        super().__init__(self)
        #Base Infos
        self.self_id = "" #The Unique ID
        self.name = "" #The Name
        self.house_name = "" #For easy access
        self.house = [] #Which house the Character belongs to
        self.sex = "" #Male or Female
        self.age = 0 #What age the Character is
        self.health = 0 #Health, influences how old a Character can get
        #Family Infos; Infos about the Characters family
        self.father = [] #The Father
        self.father_id = "" #For easy access
        self.mother = [] #The Mother
        self.mother_id = "" #For easy access
        self.partner = [] #The Spouse
        self.partner_id = "" #For easy access
        self.children = [] #List of all their children
        self.preg_recov_counter = 0 #How long until the character can have kids again, if they are female
        #Location Infos; Where the Character is
        #Genetic Infos; Infos about the genes of the Character
        self.arcanlevel = 0 #16; 14; 10; 8; 7; 4; 2 
        self.magi = "" #God; Lesser God; Demi-God; Godblood; Pureblood; Blueblood; Mundane
        #Status Infos; Infos about the Characters birth and death
        self.birth_d = "" #The birth year
        self.death_d = "" #The death year
        self.alive = True #If the Character is alive
        #Property Infos; What the Character owns
        self.land = 0 #How much land the Character owns
        self.wealth = 0 #How much money the Character has
        #Other Infos; Everything that doesn't fit in the above
        self.rank = "" #The rank the Character has in society; Possible ranks are: Freeman/Freewoman, Burgher, Patrician, Minor Noble, Greater Noble, Royal; Based on the amount of land they have

    def pregnacy(self):
        if self.preg_recov_counter == 0:
            mother = self
            self.birth(mother)
        else:
            self.preg_recov_counter = self.preg_recov_counter-1
        
    def birth(self, mother):
        mother = self
        mother_id = self.unique_id
        father = self.spouse[0]
        father_id = self.spouse_id
        i = len(total_population)
        child = character(i, self)
        child.father_id = father_id
        child.father = father
        child.mother_id = mother_id
        child.mother = mother
        child.arcanelevel = int((father.arcanelevel+mother.arcanelevel)/2) #Gives the median value of parents arcanelevel; Always rounds down
        child.firstname()
        if father.lastname == "":
            if child.sex == "Male":
                child.patronym = str(father.name)+"ssohn"
            elif child.sex == "Female":
                child.patronym = str(father.name)+"stochter"
        else:
            child.lastname = father.lastname
        child.birth_year = year
        mother.children.append(child)
        father.children.append(child)
        total_population.append(child)
        living_population.append(child)
        simulation.schedule.add(child)
        rn = random.randint(0, 100)
        if rn =< 20:
            mother.preg_recov_count = 3
        elif rn =<40:
            mother.preg_recov_count = 4
        elif rn =< 60:
            mother.preg_recov_count = 5
        elif rn =< 80:
            mother.preg_recov_count = 4
        else:
            mother.preg_recov_count = 2

        def get_firstname(self):
            if self.sex == "Male":
                self.name = random.choice(MaleNames)
            else:
                self.name = random.choice(FemaleName)
                
        def get_lastname(self):
            father = self.father
            if current_year => start_year+200:
                if father.lastname =! "":
                   self.lastname = father.lastname
                else:
                    rn = random.randint(0,1)
                    if rn == 0:
                        self.lastname = random.choice(Lastnames)
                    else:
                        self.lastname = self.patronym

        def step(self):
            pass
        
class house():
    def __init__(self):
        super().__init__(self)
        #Base Infos
        self.self_id = ""
        self.name = ""
        self.members = [] #List of all the house members
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
        self.owner = [] #Who holds the title
        self.vassals = [] #Who the title rules over
        self.liege = [] #Which title's subject it is; can never be of an higher tier then the liege
class core(Model): #Here comes all the action
    def __init__(self):
        pass
simulation = core() #Don't change
