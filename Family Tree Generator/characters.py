from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random
import csv
import webbrowser

##TODO
#Replace lists with dicts were possible

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

sexList = ["Male", "Female"]
sex = ""
N = 20 #Starting population
S = 1 #Starting settelments
#Beware here be lists
total_population = [] #Total population from start to end
population = [] #Currently alive population
valid_partner = [] #Valid Partners

current_place = ""
age = 0
birth_year = ""
death_year = ""
human = 0
orc = 0

###Vars for settelments###
p_names = ["Grauburg", "Grauhof", "Salzberg", "Goldtor", "Ostburg", "Westhof", "Ebedorf", "Grauhafen", "Wilhelmshof"]
s_list = []
###Ideologic positions###
i_race_mixingList = ["Xenophobe", "Xenophile"] #What position a person has on breeding with Orcs and other such races
i_rulership = ["Hereditary", "Election"] #What position a person has on how leaders should be choosen

###General Vars###
year = 100 #Current Year
end_year = 400 #Last Year
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

class settelment(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = ""
        self.population = []
        self.neighbors = []
        self.unhappy = []
        self.orcs = 0 #Orcs
        self.humans = 0 #Humans
        self.halfs = 0 #Half-Orcs
    def update(self):
        self.orcs = 0
        self.humans = 0
        self.halfs = 0
        for p in range(len(self.population)):
            ##BUG - Why the fuck does it say this is a list object!?!##
            person = self.population[p-1]
            if person.race == "Human":
                self.humans +=1
            elif person.race == "Orc":
                self.orcs +=1
            else:
                self.halfs +=1
    
    def step(self):
        if len(self.population) >= 1:
            self.update()
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
        self.health = random.randint(0, 4)+0.2
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

        #Personality Stuff
        #i = _i_deology
        self.stubborness = 0
        self.i_race_mixing = "" #Does the person want to mix with members of other races? For example does the human want to marry another human or are they open to other races? 
        
    def death(self, population):
        sp = len(self.current_place)-1
        s = self.current_place[sp]
        self.alive = False
        self.death_year = year
        self.death_p = self.current_place_name
        s.population.remove(self) #Remove the agent from the alive population
        run_model.schedule.remove(self) 
    def age_update(self, population, total_population):
        self.age = self.age+1
        if self.age <= 20:
            self.health +=0.2
        elif self.age >= 25:
            self.health -=0.1
        #KILL THEM ALL!
        if self.health <= 2:
            health_score = 2/self.health
            if random.randint(0, 100)*health_score >= 60:
                self.death(population)
        
    def find_partner(self, population):
        #pre-select partners
        s = self.current_place[0]
        valid_partner.append(0)
        valid_partner.clear()
        #ps_target: Pre-Select Target
        for ps_target in range(len(s.population)-1):
            #in the end add all valid people to valid_partner
            ps_target = s.population[ps_target]
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
            while s_target.spouse_id != "" and sg <= 10:
                s_target = random.randint(0, len(valid_partner)-1)
                s_target = valid_partner[s_target]
                sg = sg+1   
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
        s = self.current_place[0]
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
                        mother.preg_recov_count = 4
                    elif ri < 90:
                        mother.preg_recov_count = 5
                    else:
                        mother.preg_recov_count = 3
                    ri = 0
                child.human = (father.human+mother.human)/2
                child.orc = (father.orc+mother.orc)/2
                if child.orc >= 0.25 and child.orc <= 0.75:
                    child.race = "Half-Orc"
                    child.i_race_mixing = "Xenophile"
                elif child.orc >= 0.75:
                    child.race = "Orc"
                    ra = random.randint(0, 5)
                    if ra <= 3:
                        child.i_race_mixing = "Xenophobe"
                    elif ra >= 4:
                        child.i_race_mixing = "Xenophile"
                elif child.orc <= 0.25:
                    child.race = "Human"
                    child.i_race_mixing = random.choice(i_race_mixingList)
                child.get_name()
                child.birth_p = s.name
                child.current_place_name = s.name
                child.current_place.append(s)
                s.population.append(child)
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
    def __init__(self, S, N):
        self.setup_settelment(S, N)
    def setup_settelment(self, S, N):
        self.s_schedule = RandomActivation(self)
        for j in range(S):
            new_id = j-1
            s = settelment(new_id, self)
            s.name = random.choice(p_names)
            j = j-1
            s_list.append(s)
            self.s_schedule.add(s)
            self.setup_person(N, j)
    def setup_person(self, N, j):
        #create people
        self.schedule = RandomActivation(self) #Schedule for ze people!
        for i in range(N):
            #Some basic shit to set up the starting population
            s = s_list[j]
            p = person(i, self)
            p.age = 20
            p.health = random.randint(4, 8)
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
            p.i_race_mixing = "Xenophobe"
            p.get_name()
            p.current_place_name = s.name
            p.current_place.append(s)
            s.population.append(p)
            total_population.append(p)
            self.schedule.add(p)
    def step(self):
        self.schedule.step()
        self.s_schedule.step()

#Run the code
run_model = WorldModel(S, N)
file = open("save_file_2.csv", "w", newline="")
census = open("census.csv", "w", newline = "")
census.write("Year; Total Population; Human Population; Orc Population; Half-Orc Population\n")
for i in range(end_year):
    for s in range(len(s_list)):
        S = s_list[s-1]
        hum = 0
        trc = 0
        hor = 0
        for j in range(len(S.population)):
            p = S.population[j]
            if p.race == "Human":
                hum = hum+1
            elif p.race == "Orc":
                trc = trc+1
            elif p.race == "Half-Orc":
                hor = hor+1
        census.write(str(year)+";"+str(len(S.population))+";"+str(hum)+";"+str(trc)+";"+str(hor)+"\n")
        hum = 0
        trc = 0
        hor = 0
        print(len(s_list))
        #print("\n"+str(S.name)+" Population: "+str(len(S.population)))
    run_model.step()
    year = year+1 
#Saving and shieeeet
file.write("Unique ID; Name; Patronym; Lastname; Sex; Father ID; Mother ID; Spouse ID; Birth; Death; Age; Race; Human%; Orc%"+"\n")
living = 0
for i in total_population:
    if i.alive == True:
        living+=1
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.patronym)+";"+str(i.lastname)+";"+str(i.sex)+";"+str(i.father_id)+";"+str(i.mother_id)+";"+str(i.spouse_id)+";"+str(i.birth_year)+";"+str(i.death_year)+";"+str(i.age)+";"+str(i.race)+";"+str(i.human*100)+";"+str(i.orc*100)+"\n")
print("\n""The End | Total Population: "+str(living)) #Beatings will continue until moral and code improve!
file.close()
census.close()
