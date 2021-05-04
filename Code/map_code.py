import custom_lib as cl
import math as m
import random as r


class settlement():
    def __init__(self):
        self.uid = None #A unique ID
        self.pos_x = None
        self.pos_y = None

        self.name = "" #Name of the place
        self.inhabitans = [] #List of people living here
        self.avaible_males = []
        self.avaible_females = []
        self.neighbors = []
        
        self.desirability = 0 #How desirable the place is
        self.development = 0 #How developt the settlement is

        self.local_k = 0 #How many people can be supported
        self.effectiv_k = 0 #After all the modifiers are applied to local_k

    def update(self):
        self.effectiv_k = self.local_k + self.local_k * self.development #Gives a minimum of people that cna live here
        self.development = self.calc_development()
        self.desirability = self.calc_desirability()
        kp_ratio = round(1-(len(self.inhabitans)/self.effectiv_k), 4)
        if 0 < len(self.inhabitans):
            self.update_avaibility()
            queue = self.inhabitans
            r.shuffle(queue)
            #Fun with people
            for i in range(len(queue)):
                try:
                    person = queue[i]
                    person.update(kp_ratio)
                except IndexError:
                    break

    def calc_development(self):
        development = self.development
        if len(self.inhabitans) < (self.effectiv_k * 0.1):
            development = development - development * 0.02
        elif (self.effectiv_k * 0.1) < len(self.inhabitans):
            development = development + development * 0.01
            
        return(development)

    def calc_desirability(self):
        try:
            desirability = (self.development * 0.2) + (1-(len(self.inhabitans)/self.effectiv_k))*10
        except ZeroDivisionError:
            desirability = (self.development * 0.2) + 10
        desirability = round(desirability, 4)

        return(desirability)

    def update_avaibility(self):
        for i in range(len(self.inhabitans)):
            person = self.inhabitans[i]
            if person.alive == False:
                pass
            elif len(person.spouse) == 0 and person not in self.avaible_males and person not in self.avaible_females:
                if person.sex == 0:
                    self.avaible_males.append(person)
                else:
                    self.avaible_females.append(person)
            elif (len(person.spouse) == 0 or 50 < person.age) and person in self.avaible_males or person in self.avaible_females:
                if person.sex == 0:
                    self.avaible_males.remove(person)
                else:
                    self.avaible_females.remove(person)         

    def create(self, uid, name, local_k, x, y, mortality):
        self.uid = uid
        self.pos_x = x
        self.pos_y = y
        self.name = name
        self.local_k = local_k
        self.local_child_mortality = mortality

        self.update()

    def add_neighbor(self, start, end):
        start.neighbors.append(end)
        end.neighbors.append(start)

    def move_person(self, person, target):
        self.inhabitans.remove(person)
        target.inhabitans.append(person)
        person.location.clear()
        person.location.append(target)


class region():
    def __init__(self):
        self.uid = 0
        self.name = "Placeholder"

        self.places = [] #Either contains list of other regions or settlements

    def update(self):
        for i in range(len(self.places)):
            place = self.places[i]
            place.update()

    def create(self, uid, name):
        pass

    def create_settlements(self):
        file = cl.txt_to_list("../Input/map.txt")
        #Change this if the format of the map.txt changes
        count = int(file[1]) #Gets the amount of settlements to be added from the file
        file.pop(0)
        file.pop(0)
        for i in range(count):
            uid = int(file[0])
            name = file[1]
            x = int(file[2])
            y = int(file[3])
            k = int(file[4])
            m = 0.007
            s = settlement()
            s.create(uid, name, k, x, y, m)
            self.places.append(s)
            for ii in range(5):
                file.pop(0)

    def set_up_map(self):
        self.create_settlements()
        for i in range(len(self.places)):
            place1 = self.places[i]
            for ii in range(len(self.places)):
                place2 = self.places[ii]
                if place1 != place2:
                    dist = self.calc_distance(place1, place2)
                    if dist <= 10:
                        place1.add_neighbor(place1, place2)

    def calc_distance(self, start, end):
        x = end.pos_x - start.pos_x
        y = end.pos_y - start.pos_y

        dist = m.sqrt(x*x + y*y)

        return(dist)

    def return_population(self):
        p = 0
        for i in range(len(self.places)):
            place = self.places[i]
            p = p + len(place.inhabitans)
        return(p)
    