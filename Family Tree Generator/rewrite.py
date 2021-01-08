
import numpy as np
import random as r
import csv
import webbrowser
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import networkx as nx
import matplotlib.pyplot as plt
#Read Me
##TODO:
###Add all the Values needed

total_population = [] #List of all people to have ever lived
living_population = []
valid_partners = []
house_list = []
current_year = 0 #The current year
start_year = 0 #The year the sim starts
end_year = 100 #The year the sim ends
age_of_the_world = "" #Which age the world is in; List of Ages: Age of Myth, Age of Legend, Age of Heros, etc
starting_population = 40
sexes = ["Male", "Female"]
#Coded inputs

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
        self.unique_id = "" #The Unique ID
        self.name = "" #The Name
        self.lastname = ""
        self.sex = "" #Male or Female
        self.age = 0 #What age the Character is
        self.health = 0 #Health, influences how old a Character can get
        #Family Infos; Infos about the Characters family
        self.father = [] #The Father
        self.father_id = "" #For easy access
        self.mother = [] #The Mother
        self.mother_id = "" #For easy access
        self.partner = [] #The Spouse
        self.spouse_id = "" #For easy access
        self.children = [] #List of all their children
        self.preg_recov_counter = 0 #How long until the character can have kids again, if they are female
        #Location Infos; Where the Character is
        #Genetic Infos; Infos about the genes of the Character
        self.arcanlevel = 0 #16; 14; 10; 8; 7; 4; 2 
        self.magi = "" #God; Lesser God; Angle; Demi-God; Godtouched; Pureblood; Mundane
        #Status Infos; Infos about the Characters birth and death
        self.birth_d = "" #The birth year
        self.death_d = "" #The death year
        self.alive = True #If the Character is alive
        #Property Infos; What the Character owns
        self.land = 0 #How much land the Character owns
        self.wealth = 0 #How much money the Character has
        #Other Infos; Everything that doesn't fit in the above
        self.rank = "" #The rank the Character has in society; Possible ranks are: Freeman/Freewoman, Burgher, Patrician, Minor Noble, Greater Noble, Royal; Based on the amount of land they have
        self.traits = []
        
    def pregnacy(self):
        if self.preg_recov_counter == 0:
            mother = self
            self.birth(mother)
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
        child.sex = r.choice(sexes)
        child.arcanelevel = int((father.arcanelevel+mother.arcanelevel)/2-r.randint(0,1)) #Gives the median value of parents arcanelevel; Always rounds down
        child.divinity(child)
        child.health = (r.randint(1, 4)+child.arcanelevel)
        child.firstname(child)
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

    def divinity(self, child):
        target = child
        if target.arcanelevel <= 2:
            target.magi = "Mundane"
        elif target.arcanelevel <= 4:
            target.magi = "Pureblood"
        elif target.arcanelevel <= 7:
            target.magi = "Godtouched"
        elif target.arcanelevel <= 8:
            target.magi = "Demi-God"
        elif target.arcanelevel <= 10:
            target.magi = "Angle"
        elif target.arcanelevel <= 14:
            target.magi = "Lesser God"
        elif target.arcanelevel <= 16:
            target.magi = "God" 
        else:
            target.arcanelevel = 1
            target.magi = "Mundane"
            
    def get_firstname(self, target):
        named = target
        if named.sex == "Male":
            named.name = r.choice(MaleNames)
        else:
            named.name = r.choice(FemaleNames)
            
    def get_lastname(self):
        father = self.father
        if current_year >= start_year+200:
            if father.lastname != "":
               self.lastname = father.lastname
            else:
                rn = r.randint(0,1)
                if rn == 0:
                    self.lastname = r.choice(Lastnames)
                else:
                    self.lastname = self.patronym

    def find_partner(self):
        valid_partner = []
        valid_partner.append(0)
        valid_partner.clear()
        vpr = len(valid_partners)
        for i in range(vpr):
            target = valid_partners[i]
            if ((target != self) and
                (target.father_id != self.father_id) and
                (target.sex != self.sex) and
                (target.age <= 45 and target.age >= 16) and
                (target.spouse_id == "")
                ):
            #########################################
                valid_partner.append(target)
            else:
                pass
        if len(valid_partner) > 0:
            k = r.randint(0, len(valid_partner))
            target = valid_partner[k]
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
            valid_partners.remove(self)
        else:
            valid_partners.append(self)
        if self.health <= 0:
           self.death()

    def death(self):
        self.alive = False
        living_population.remove(self)
        self.death_d = current_year
        core().schedule.remove(self)
    
    def step(self):
        if self.alive == True: #Safe guard
            self.age_update()
            if self.spouse_id == "":
                self.find_partner()
            else:
                pass
            if self.sex == "Female" and self.spouse_id == True:
                spouse = self.spouse[0]
                if spouse.alive == True:
                    self.pregnacy()
        
class title():
    def __init__(self):
        super().__init__(self)
        self.title_id = ""
        self.tier = "" #Which tier the Title is; Duchy for example
        self.prefix = "" #How the owner is called; Duke for example
        self.name = ""
        self.settelments = [] #Settelments that are ruled by the title
        self.owner = [] #Who holds the title
        self.vassals = [] #Who the title rules over
        self.liege = [] #Which title's subject it is; can never be of an higher tier then the liege
        
class core(Model): #Here comes all the action
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.setup_population(starting_population)
        
    def setup_population(self, starting_population):
        for i in range(starting_population):
            p = character(i, self)
            p.age = 20
            p.birth_d = start_year-p.age
            p.sex = r.choice(sexes)
            p.arcanelevel = r.randint(10, 16)
            p.health = r.randint(3, 6)+p.arcanelevel
            p.divinity(p)
            p.get_firstname(p)
            living_population.append(p)
            total_population.append(p)
            valid_partners.append(p)
            self.schedule.add(p)
    def step(self):
        self.schedule.step()
current_year = start_year            
simulation = core() #Don't change
print("Start generation...")
for year in range(start_year, end_year):
    simulation.step()
    current_year = current_year+1
print("Finished generation...")
