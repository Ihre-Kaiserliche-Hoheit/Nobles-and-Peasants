import numpy as np
import random as r
import csv
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler

#Settings
current_year = 0 #The current year
start_year = 100 #The year the sim starts
end_year = 400 #The year the sim ends
starting_population = 20 #How many squishy humans exist at the beginning
pop_celling = 1500 #At which population sice the culling beginns

#Not Settings
total_population = [] #List of all people to have ever lived
living_population = []
valid_spouses = [] #List of everyone in the age range of 16 - 45, that isn't married
valid_spouse = [] #Maybe can be removed?
sexes = ["Male", "Female"] #Don't bitch, it's the easiest way to give people a random sex at birth
fzu = 6 #Family Size Upper limit; How many childrne people want at most, smaller number = slower growth


#Setup
print("Starts...")
print("Load names...")
#Import the namelists from .txt files and convert them to lists
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
        self.name = "" #The Name
        self.patronym = "" #Patronyms are fun
        self.lastname = ""
        self.sex = "" #Male or Female
        self.age = 0 #What age the Character is
        self.health = 0 #Health, influences how old a Character can get
        #Family Infos; Infos about the Characters family
        self.father = [] #The Father
        self.father_id = "" #For easy access
        self.mother = [] #The Mother
        self.mother_id = "" #For easy access
        self.spouse = [] #The Spouse
        self.spouse_id = "" #For easy access
        self.children = [] #List of all their children
        self.family_size = "" #How many children they want; Limits the size of population booms, only important for woman
        self.preg_recov_counter = 0 #How long until the character can have kids again, if they are female
        #Status Infos; Infos about the Characters birth and death
        self.birth_d = "" #The birth year
        self.death_d = "" #The death year
        self.alive = True #If the Character is alive
        
    def pregnacy(self):
        #Checks if a woman can have a kid
        if self.family_size <= len(self.children):
            self.preg_recov_counter = 1
        elif self.preg_recov_counter <= 0:
            mother = self
            mother.birth(mother)
        else:
            self.preg_recov_counter = self.preg_recov_counter-1
            
    def preg_counter(self):
        self.preg_recov_count = r.randint(2, 6) #Tweak until population growth is at a good level

    def birth(self, mother):
        #Creates a new character and bla bla
        mother_id = mother.unique_id
        father = mother.spouse[0]
        father_id = mother.spouse_id
        C = len(total_population)+1
        child = character(C, Model)
        child.father_id = father_id
        child.father = father
        child.mother_id = mother_id
        child.mother = mother
        child.sex = r.choice(sexes)
        child.health = (r.randint(2, 4))
        child.family_size = r.randint(1, fzu)
        child.get_firstname(child)
        if father.lastname == "":
            if child.sex == "Male":
                child.patronym = str(father.name)+"ssohn"
            elif child.sex == "Female":
                child.patronym = str(father.name)+"stochter"
            child.get_lastname
        else:
            child.lastname = father.lastname
        child.birth_d= current_year
        mother.children.append(child)
        father.children.append(child)
        total_population.append(child)
        living_population.append(child)
        simulation.schedule.add(child)
        mother.preg_counter()

    def get_firstname(self, target):
        #You get a name, you get a name, EVERYONE GETS A NAME
        named = target
        if named.sex == "Male":
            named.name = r.choice(MaleNames)
        else:
            named.name = r.choice(FemaleNames)

    def get_lastname(self):
        #Gives people lastnames
        father = self.father
        if current_year > (start_year+200): #start_year+200 can be changed to start_year+0 if need be
            if self.lastname == "":
                rn = r.randint(0,1)
                if rn == 0:
                    self.lastname = r.choice(Lastnames)
                else:
                    self.lastname = self.patronym

    def find_spouse(self):
        #Explaination of what the code SHOULD do:
        #First 200 random people are chosen from the living,
        #then each one is checked if they are viable spouses[see if statment for conditions]
        #this is followed by checking if the list is equal to or larger than 1,
        #the last step is picking one of the viable characters and add them as spouse

        #Reasoning behind the chosing 200 randos
        #1 - The goal is to represent the lack of awareness of every possible partner
        #2 - The other goal is to decrease the rate of slowing in larger [1000+] population
        valid_spouse = []
        spouse_choice = r.choices(valid_spouses, k=200)
        vpr = len(spouse_choice)
        for i in range(vpr):
            target = spouse_choice[i]
            if ((target != self) and
                ((target.father_id != self.father_id) or (target.father_id == "" and self.father_id == "")) and
                (target.sex != self.sex) and
                (target.age <= 45 and target.age >= 16) and
                (target.spouse_id == "")
                ):
                valid_spouse.append(target)
            else:
                pass
        if len(valid_spouse) >= 1:
            target = r.choice(valid_spouse)
            #And now kiss
            self.spouse.append(target)
            target.spouse.append(self)
            target.spouse_id = self.unique_id
            self.spouse_id = target.unique_id

    def age_update(self):
        #Update the age/Check if they should die/Be removed from the pool of possible partners
        self.age = self.age+1
        if self.age < 20:
            self.health = self.health+1
        elif self.age > 25:
            self.health = self.health-0.5
        else:
            pass
        if self.age >= 45:
            ind = valid_spouses.index(self)
            if valid_spouses.index(self) == True: #Checks if they are in the list
                valid_spouses.remove(self) #Removes them from the list
        else:
            valid_spouses.append(self) #Add to the pool of viable spouses
        if self.health <= 0:
           self.death(self)

    def death(self, dyee):
        #SHOULD remove dead people from the realm of the living for good
        dyee.alive = False
        living_population.remove(dyee)
        dyee.death_d = current_year
        simulation.schedule.remove(dyee)
        
    def step(self):
        if self.alive == True: #Safe guard
            self.age_update()
            self.get_lastname() #Why the fuck didn't I add brackets here? Now it should work
            if self.spouse_id == "":
                self.find_spouse()
            else:
                pass
            if self.sex == "Female" and self.spouse_id != "":
                spouse = self.spouse[0]
                if spouse.alive == True:
                    self.pregnacy()
        
class core(Model): #Here comes all the action
    def __init__(self): 
        self.setup_population(starting_population)
        
    def setup_population(self, starting_population):
        self.schedule = RandomActivation(self)
        for i in range(starting_population):
            p = character(i, self)
            p.age = 20
            p.birth_d = start_year-p.age
            p.sex = r.choice(sexes)
            p.family_size = r.randint(1, fzu)
            p.health = r.randint(4, 8)
            p.get_firstname(p)
            living_population.append(p)
            total_population.append(p)
            valid_spouses.append(p)
            self.schedule.add(p)

    def dead_filter(self, deaths):
        possible_deaths = r.choices(living_population, k=deaths)
        soon_ded = []
        for i in range(len(possible_deaths)):
            victim = possible_deaths[i]
            if  (((victim.age > 4) and (victim.age < 12)) or
                (victim.age > 30)
                ): #Kill the brats and old!
                soon_ded.append(victim)
        #print(len(soon_ded))
        possible_deaths.clear()
        self.big_dead(soon_ded)
        
    def big_dead(self, soon_ded): #Event to cull big populations, cuz fuck em
        #This thing only exist because the populations grew to big and slowed the programm down too much.
        #Now the population will stay somewhere below 2500 people.
        #Why 2500 you ask? Simple, the porgram basicly dies once the number goes above 3000 characters and
        #Already starts to slow at 2000, so I chose 2500 as an good upper limit
        #
        #TODO
        #Make the code chose older characters over younger ones
        #soon_ded = r.choices(living_population, k=deaths)
        for i in range(len(soon_ded)):
            sd = soon_ded[i]
            if sd.alive == True:
                sd.death(sd)
        soon_ded.clear()
        
    def step(self):
        self.schedule.step()

current_year = start_year #It's current year, duh
simulation = core() #Don't change the name
starting_population = 0 #Can maybe be removed savely

print("Start generation...")
for year in range(start_year, end_year):
    simulation.step()
    if len(living_population) >= pop_celling:
            d = int(round(len(living_population)/3, 0)) #d is the amount of soon to be dead
            simulation.dead_filter(d)
    current_year = current_year+1
    if current_year % 10 == 0:
        print("Year: "+str(current_year)+" "+str(len(living_population)))

print("\n""The End | Total Population: "+str(len(living_population)))
print("Finished generation...")
file = open("save_file.csv", "w+", newline="")
file.write("Unique ID; Name; Patronym; Lastname; Sex; Father ID; Mother ID; Spouse ID; Birth; Death; Age"+"\n")
for j in range(len(total_population)):
    i = total_population[j]
    file.write(str(i.unique_id)+";"+str(i.name)+";"+str(i.patronym)+";"+str(i.lastname)+";"+str(i.sex)+";"+str(i.father_id)+";"+str(i.mother_id)+";"+str(i.spouse_id)+";"+str(i.birth_d)+";"+str(i.death_d)+";"+str(i.age)+"\n")
file.close()
print("End of Program!")
