import numpy as np
import random
import csv
import webbrowser

#Read Me
##TODO:
###Add all the Values needed

total_population = []

class character(self):
    def __init__(self):
        super().__init__(self)
        #Base Infos
        self.self_id = "" #The Unique ID
        self.name = "" #The Name
        self.lastname = ""
        self.sex = "" #Male or Female
        self.age = 0 #What age the Character is
        self.health = 0 #Health, influences how old a Character can get
        #Family Infos; Infos about the Characters family
        self.father = []
        self.father_id = "" #For easy access
        self.mother = []
        self.mother_id = "" #For easy access
        self.partner = []
        self.partner_id = "" #For easy access
        self.children = [] #List of all their children
        self.preg_recov_counter = 0 #How long until the character can have kids again, if they are female
        #Location Infos; Where the Character is
        #Status Infos; Infos about the Characters birth and death
        self.birth_d = "" #The birth year
        self.death_d = "" #The death year
        self.alive = True #If the Character is alive
        #Property Infos; What the Character owns
        #Other Infos; Everything that doesn't fit in the above
