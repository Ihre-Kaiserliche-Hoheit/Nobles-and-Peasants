import numpy as np
import random
import csv
import webbrowser
from mesa import Model
import Map

#Read Me
##TODO:
###Add all the Values needed

total_population = [] #List of all people to hace ever lived
current_year = 0 #The current year
start_year = 0 #The year the sim starts
end_year = 0 #The year the sim ends
age_of_the_world = "" #Which age the world is in; List of Ages: Age of Myth, Age of Legend, Age of Heros, etc

#Coded inputs
map_size = 25

class character():
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
        self.race = "" #Human, Orc or Half-Orc?
        self.orc = 0 #self.human+self.orc should always add up to 1
        self.human = 0
        #Status Infos; Infos about the Characters birth and death
        self.birth_d = "" #The birth year
        self.death_d = "" #The death year
        self.alive = True #If the Character is alive
        #Property Infos; What the Character owns
        self.land = 0 #How much land the Character owns
        self.wealth = 0 #How much money the Character has
        #Other Infos; Everything that doesn't fit in the above
        self.ideology = "" #What the person beliefs in
        self.culture = ""
        self.religion = ""
        self.rank = "" #The rank the Character has in society; Possible ranks are: Slave, Serf, Freeman/Freewoman, Burgher, Patrician, Minor Noble, Greater Noble, Royal
        self.titles = [] #The title the Character has; Possible titles are: Yeoman(Freeman up to Patrician), Gentleman/Lady(Patrician up to Minor Noble), Esquire(Minor Noble), Knight/Dame(Minor Noble), Baronet/Baronetess(Minor Noble), Baron/Baroness(Minor Noble), Viscount/Viscountess(Minor Noble), Count/Countess(Minor Noble up to Greater Noble),  Margrave(Minor Noble up to Greater Noble),  Duke/Duchess(Greater Noble), Grand Duke/Duchess(Greater Noble up to Royal), Prince/Princess(Higher Noble up to Royal), Crown Prince/Princess(Royal), King/Queen(Royal), Emperor/Empress(Royal)
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
class settelment():
    def __init__(self):
        super().__init__(self)
        self.position = [] #The tile of the settelment
        self.corrds_x = ""
        self.corrds_y = ""
        self.land = 0 #How much land belongs to the settelment
        self.population = [] #How many people live here
        self.population_count = 0 #Total Population
        self.kind = "" #Is it a village, town, city or something entirly different?
        self.title = [] #Which title the settelment belongs to
    def create_settelment(self):
        pass
    def update(self):
        pass
    def step(self):
        pass
class core(): #Here comes all the action
    def __init__(self):
        pass
    def setup_map(self):
        pass
    def setup_chars(self):
        pass
    def step():
        pass
#Action Zone
World = Map.Map()
