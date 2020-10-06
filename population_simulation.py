#This File only exists to test different code bits and pieces
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random
import csv
import webbrowser
import weakref
import os

###Vars from the Person class###

#Names for human men
HumanListM = []
#Names for human women
HumanListF = []
#Lastnames/Surenames for humans
HumanListL = []
#Names for orc men
OrcListM = []
#Names for orc women
OrcListF = []
#Lastnames for orcs
OrcListL = []
#zal mean of

sexList = ["Male", "Female"]

sex = ""
N = 20 #Starting population
#Beware here be lists
total_population = [] #Total population from start to end
population = [] #Currently alive population
valid_partner = [] #Valid Partners; Meta value

current_place = ""
age = 0
birth_year = ""
death_year = ""
human = 0
orc = 0

###Vars from the Place class###
place_kinds = ["Farming Village"]
places = []
p_kind = ""
p_names = ["Grauburg"]
inhabitans = [] 
total_land = 0
free_land = 0
food_storage = 0
i_race_mixingList = ["Xenophobe", "Xenophile"]

###General Vars###
year = 1 #Current Year
end_year = 200 #Last Year
#Notes:
#A start population of 10 over 150 steps will have a finial population of around 300+/-100 based on how unbalanced the start sex ratio is and if RNGesus likes you
#!!!!!NEVER insert 0 as generic relation ANYWHERE!!!!!
HumanM = open("HumanMaleNames.txt", "r", newline="")
HumanF = open("HumanFemaleNames.txt", "r", newline="")
HumanL = open("HumanLastNames.txt", "r", newline="")
OrcL = open("OrcLastNames.txt", "r", newline="")
OrcM = open("OrcMaleNames.txt", "r", newline="")
OrcF = open("OrcFemaleNames.txt", "r", newline="")
HumanListM = HumanM.read().splitlines()
HumanListF = HumanF.read().splitlines()
HumanListL = HumanL.read().splitlines()
OrcListM = OrcM.read().splitlines()
OrcListF = OrcF.read().splitlines()
OrcListL = OrcL.read().splitlines()
OrcL.close()
OrcF.close()
OrcM.close()
HumanL.close()
HumanF.close()
HumanM.close()
#HumanListM = [line.split("\n") for line in HumanM]
file = open("save_file_2.csv", "w", newline="")
census = open("census.csv", "w", newline = "")

class person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #Genetic Stuff
        self.human = human
        self.orc = orc
        self.race = ""
        sex = random.choice(sexList)
        self.name = ""
        self.patronym = ""
        self.lastname = ""
        self.sex = sex
        self.age = age
        self.health = random.randint(4, 8)
        self.job = ""
        self.birth_year = birth_year
        self.death_year = death_year
        self.current_place_name = ""
        self.current_place = []
        self.birth_p = ""
        self.death_p = ""
        self.father = []
        self.father_id = ""
        self.mother = []
        self.mother_id = ""
        self.spouse = []
        self.spouse_id = ""
        self.children = []     
        self.alive = True
        self.preg_recov_count = 0

        #Political Stuff
        #i = _i_deology
        i_race_mixing = random.choice(i_race_mixingList)
        self.i_race_mixing = i_race_mixing #Does the person want to mix with members of other races? For example does the human want to marry another human or are they open to other races?

        
        
        
    def death(self, population):
        self.alive = False
        self.death_year = year
        population.remove(self) #Remove the agent from the alive population
        run_model.schedule.remove(self)
        
    def age_update(self, population, total_population):
        age = self.age
        age = age+1
        self.age = age
        if age >= 25:
            self.health -=0.1
        #KILL THEM ALL!
        if age <= 6:
            if age >= 0 and age <= 2:
                if random.randint(0, 100) < 20: #This should be a 20% chance of dying
                    self.death(population)
            elif age >= 3 and age <= 4:
                if random.randint(0, 100) < 10: #This should be a 10% chance of dying
                    self.death(population)
            elif age >= 5 and age <= 6:
                if random.randint(0, 100) < 5: #This should be a 5% chance of dying
                    self.death(population)
        if self.health <= 2:
            health_score = 2/self.health
            if random.randint(0, 100)*health_score >= 60:
                self.death(population)
        
    def find_partner(self, population):
        #pre-select partners
        valid_partner.append(0)
        valid_partner.clear()
        #ps_target: Pre-Select Target
        for ps_target in range(len(population)-1):
            #in the end add all valid people to valid_partner
            ps_target = population[ps_target]
            if ps_target.spouse_id != "":
                pass
            else:
                if self.i_race_mixing == "Xenophile":
                    if self.current_place == ps_target.current_place:
                        if self == ps_target:
                            pass
                        elif self != ps_target:
                            if self.sex == ps_target.sex:
                                pass
                            elif self.sex != ps_target.sex:
                                if self.spouse_id != "":
                                    pass
                                else:
                                    #No Incest
                                    if (ps_target.father_id == "" and self.father_id == "") or (ps_target.mother_id == "" and self.mother_id == ""):
                                        valid_partner.append(ps_target)
                                    else:
                                        if ps_target.father_id == self.father_id or ps_target.mother_id == self.mother_id:
                                            pass
                                        else:
                                            valid_partner.append(ps_target)
                                            
                elif self.i_race_mixing == "Xenophobe":
                    if self.race == ps_target.race:
                        if self.current_place == ps_target.current_place:
                            if self == ps_target:
                                pass
                            elif self != ps_target:
                                if self.sex == ps_target.sex:
                                    pass
                                elif self.sex != ps_target.sex:
                                    if self.spouse_id != "":
                                        pass
                                    else:
                                        #No Incest
                                        if (ps_target.father_id == "" and self.father_id == "") or (ps_target.mother_id == "" and self.mother_id == ""):
                                            valid_partner.append(ps_target)
                                        else:
                                            if ps_target.father_id == self.father_id or ps_target.mother_id == self.mother_id:
                                                pass
                                            else:
                                                valid_partner.append(ps_target)
                else:
                    pass
        #chose random person from the valid partner list
        #s_target: Select Target
        if len(valid_partner) > 0:
            s_target = random.randint(0, len(valid_partner)-1)
            while self == s_target:
                s_target = random.randint(0, len(valid_partner)-1)
            s_target = valid_partner[s_target]
            sg = 0   
            while self.sex == s_target.sex and sg <= 10:
                s_target = random.randint(0, len(valid_partner)-1)
                s_target = valid_partner[s_target]
                sg = sg+1
                #print("new partner 1") #Debug Code
            while s_target.spouse_id != "" and sg <= 10:
                s_target = random.randint(0, len(valid_partner)-1)
                s_target = valid_partner[s_target]
                sg = sg+1
                #print("new partner 2") #Debug Code
                
            #Post-selection to make sure everything is okay
            if self.sex == s_target.sex:
                if self.spouse_id != "":
                    s_target.spouse_id = ""
                elif s_target.spouse_id != "":
                    self.spouse_id = ""
                else:
                    pass
            elif self.spouse_id == self.unique_id or s_target.spouse_id == s_target.unique_id:
                if self.spouse_id == self.unique_id:
                    self.spouse_id = ""
                elif s_target.spouse_id == s_target.unique_id:
                    s_target.spouse_id = ""
            #Age restrictions! Below 16 is one big no-no
            elif self.age <= 16 or s_target.age <= 16:
                if self.age <= 16:
                    self.spouse_id = ""
                    s_target.spouse_id = ""
                elif s_target.age <= 16:
                    self.spouse_id = ""
                    s_target.spouse_id = ""
            #Sorry, but this is an milf free zone!
            elif self.age >= 45 or s_target.age >= 45:
                if self.age >= 45:
                    self.spouse_id = ""
                    s_target.spouse_id = ""
                elif s_target.age >= 45:
                    self.spouse_id = ""
                    s_target.spouse_id = ""
            else:
                self.spouse_id = s_target.unique_id
                self.spouse.append(s_target)
                s_target.spouse_id = self.unique_id
                s_target.spouse.append(self)
        sg = 0
    def have_kid(self):
        if self.sex == "Female":
            mother = self
            mother_id = self.unique_id
            father = self.spouse[0]
            father_id = self.spouse_id
        elif self.sex == "Male":
            mother = self.spouse[0]
            mother_id = self.spouse_id
            father = self
            father_id = self.unique_id
        if age <= 50:
            if mother.preg_recov_count == 0:
                i = len(total_population) #total_population, not population! If you use population you will get multiple agents with the same ID
                child = person(i, self)
                child.father_id = father_id #Save the id in the child for easier access
                child.father = father #Save link to father for easy access
                child.mother_id = mother_id #Save the id in the child for easier access
                child.mother = mother #Save link to mother for easy access
                if father.race == "Human":
                    if father.lastname == "":
                        if child.sex == "Male":
                            child.patronym = str(father.name)+"ssohn"
                        elif child.sex == "Female":
                            child.patronym = str(father.name)+"stochter"
                    else:
                        child.lastname = father.lastname
                else:
                    child.lastname = father.lastname
                
                child.birth_year = year
                child.birth_place = father.current_place
                child.current_place_name = father.current_place_name
                mother.children.append(child)
                father.children.append(child)
                while mother.preg_recov_count == 0:
                    ri = random.randint(0, 100)
                    if ri < 20:
                        mother.preg_recov_count = 2
                    elif ri < 50:
                        mother.preg_recov_count = 3
                    elif ri < 70:
                        mother.preg_recov_count = 1
                    elif ri < 90:
                        mother.preg_recov_count = 5
                    else:
                        mother.preg_recov_count = 2
                    ri = 0
                child.human = (father.human+mother.human)/2
                child.orc = (father.orc+mother.orc)/2
                if child.orc > 0.43 and child.orc <= 0.75:
                    child.race = "Half-Orc"
                elif child.orc >= 0.76:
                    child.race = "Orc"
                elif child.orc < 0.43:
                    child.race = "Human"
                child.get_name()
                population.append(child)
                total_population.append(child)
                run_model.schedule.add(child)
            elif mother.preg_recov_count >= 1:
                mother.preg_recov_count = mother.preg_recov_count-1
    def get_name(self):
        if self.race == "Orc":
            if self.sex == "Male":
                self.name = random.choice(OrcListM)
            elif self.sex == "Female":
                self.name = random.choice(OrcListF)
        elif self.race == "Half-Orc":
            if self.father == "":
                if self.race == "Human":
                    if self.sex == "Male":
                        self.name = random.choice(HumanListM)
                    elif self.sex == "Female":
                        self.name = random.choice(HumanListF)
                elif self.race == "Orc":
                    if self.sex == "Male":
                        self.name = random.choice(OrcListM)
                    elif self.sex == "Female":
                        self.name = random.choice(OrcListF)
            else:
                father = self.father
                if father.race == "Human":
                    if self.sex == "Male":
                        self.name = random.choice(HumanListM)
                    elif self.sex == "Female":
                        self.name = random.choice(HumanListF)
                elif father.race == "Orc":
                    if self.sex == "Male":
                        self.name = random.choice(OrcListM)
                    elif self.sex == "Female":
                        self.name = random.choice(OrcListF)
                elif father.race == "Half-Orc":
                    r = random.randint(0, 1)
                    if r == 0:
                        if self.sex == "Male":
                            self.name = random.choice(HumanListM)
                        elif self.sex == "Female":
                            self.name = random.choice(HumanListF)
                    elif r == 1:
                        if self.sex == "Male":
                            self.name = random.choice(OrcListM)
                        elif self.sex == "Female":
                            self.name = random.choice(OrcListF)
        else:
            if self.sex == "Male":
                self.name = random.choice(HumanListM)
            elif self.sex == "Female":
                self.name = random.choice(HumanListF)
    def get_lastname(self):
        if year <= 100:
            pass
        elif year >= 101:
            ri = random.randint(0, 100)
            if self.race == "Orc":
                self.lastname = random.choice(OrcListL)
                if not self.children:
                    pass
                else:
                    for child_l in range(len(self.children)-1):
                        child_l = self.children[child_l]
                        child_l.lastname = self.lastname
            else:
                if ri > 0 and ri < 50:
                    patronym = str(self.name)+"s"
                    self.lastname = patronym
                else:
                    self.lastname = random.choice(HumanListL)
                if not self.children:
                    pass
                else:
                    for child_l in range(len(self.children)-1):
                        child_l = self.children[child_l]
                        child_l.lastname = self.lastname
    def step(self):
        if self.alive == True:  #Only agents that are alive should do shit, duh?
            if self.age >= 16:
                if self.spouse_id == "" or self.spouse_id == -1:
                    self.find_partner(population)
                else:
                    pass
                if random.randint(0, 10) < 5:
                    if self.spouse_id != "" and self.sex == "Female":
                        self.have_kid()
                    else:
                        pass
                else:
                    pass
                if random.randint(0, 10) < 1 and not self.sex == "Female":
                    self.get_lastname()
                else:
                    pass
            self.age_update(population, total_population)
        elif self.alive == False: #Oy, and you stay dead!
            run_model.schedule.remove(self)
        else:
            print("Oi! You got a loicens for that error!?") #Should the code, for some reason, fuck up call the bobbies over!
            webbrowser.open("https://www.youtube.com/watch?v=G1IbRujko-A", new=2) #Just incase someone isn't paying tax... I mean attention!

class WorldModel(Model):
    def __init__(self, N):
        #self.setup_person(N)
        self.setup_person(N)
    def setup_person(self, N):
        #create people
        self.num_people = N
        self.schedule = RandomActivation(self) #Schedule for ze people!
        for i in range(self.num_people):
            #Some basic shit to set up the starting population
            p = person(i, self)
            p.age = 20
            p.birth_year = year-(p.age+1)
            rrace = random.randint(0, 1)
            if rrace == 1:
                p.orc = 1.0
                p.human = 0.0
                p.race = "Orc"
            else:
                p.orc = 0.0
                p.human = 1.0
                p.race = "Human"
            p.get_name()
            population.append(p)
            total_population.append(p)
            self.schedule.add(p)
    def step(self):
        self.schedule.step()
        #print("Step 1")


#Run the code
run_model = WorldModel(N)
census.write("Year; Total Population; Human Population; Orc Population; Half-Orc Population\n")
for i in range(end_year):
    hum = 0
    trc = 0
    hor = 0
    for j in range(len(population)):
        p = population[j]
        if p.race == "Human":
            hum = hum+1
        elif p.race == "Orc":
            trc = trc+1
        elif p.race == "Half-Orc":
            hor = hor+1
    census.write(str(year)+";"+str(len(population))+";"+str(hum)+";"+str(trc)+";"+str(hor)+"\n")
    hum = 0
    trc = 0
    hor = 0
    run_model.step()
    year = year+1
    print("\n"+"Total Population: "+str(len(population)))
#Saving and shieeeet
file.write("Unique ID; Name; Patronym; Lastname; Sex; Father ID; Mother ID; Spouse ID; Birth; Death; Age; Race; Human%; Orc%"+"\n")
for i in total_population:
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.patronym)+";"+str(i.lastname)+";"+str(i.sex)+";"+str(i.father_id)+";"+str(i.mother_id)+";"+str(i.spouse_id)+";"+str(i.birth_year)+";"+str(i.death_year)+";"+str(i.age)+";"+str(i.race)+";"+str(i.human)+";"+str(i.orc)+"\n")
print("\n""The End | Total Population: "+str(len(population))) #Beatings will continue until moral and code improve!
file.close()
census.close()
