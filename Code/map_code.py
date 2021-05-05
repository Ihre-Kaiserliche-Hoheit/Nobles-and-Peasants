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
        self.migrants = []
        self.neighbors = []
        self.double_neighbors = [] #List of neighbors two steps away from this place

        self.development = 0 #How developt the settlement is

        self.local_k = 0 #How many people can be supported
        self.effectiv_k = 0 #After all the modifiers are applied to local_k

    def update(self):
        self.effectiv_k = self.local_k + self.local_k * (self.development/10) #Gives a minimum of people that cna live here
        self.development = self.calc_development()
        try:
            kp_ratio = round(1-(len(self.inhabitans)/self.effectiv_k), 4)
        except ZeroDivisionError:
            kp_ratio = 0

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
            if self.local_k*0.8 < len(self.inhabitans):
                self.migration_check()

    def migration_check(self):
        """
        Checks inhabitans to get a list of migrants
        """
        migrants = self.check_for_migrants()
        self.do_migration(migrants)

    def check_for_migrants(self):
        migrants = []
        for i in range(len(self.inhabitans)):
            person = self.inhabitans[i]
            if 10 < self.calc_migration_wish(person, migrants):
                if len(person.spouse) == 0:
                    migrants.append(person)
        return(migrants)

    def do_migration(self, migrants):
        migrant_groups = []
        group_count = int(round(len(migrants)/20, 0))
        for i in range(group_count):
            group = list()
            for ii in range(20):
                try:
                    person = migrants[ii]
                    group.append(person)
                    migrants.remove(person)
                except IndexError:
                    group2 = list()
                    group2 += migrants
                    group_count +=1
                    migrant_groups.append(group2)
            migrant_groups.append(group)


        for ii in range(group_count):
            target = r.choices(self.neighbors)
            target = target[0]
            group = migrant_groups[ii]

            for i in range(len(migrants)):
                migrant = group[i]
                if migrant.alive == True:
                    start = migrant.location[0]
                    self.move_person(migrant, start, target)

    def calc_migration_wish(self, person, migrants):
        amn = len(self.avaible_males)
        awn = len(self.avaible_females)
        wish = 0
        if 20 < person.age < 25:
            wish +=20
        elif 25 <= person.age < 31:
            wish +=10

        try:
            father = person.father[0]
            if 3 < len(father.children):
                wish += 20*(len(father.children)/5)
        except IndexError:
            wish += 20

        if 30 < len(migrants):
            wish -= 10*(len(migrants)/30)

        return(round(wish, 0))


    def calc_development(self):
        development = self.development
        if len(self.inhabitans) < (self.effectiv_k * 0.1):
            development = development - development * 0.02
        elif (self.effectiv_k * 0.1) < len(self.inhabitans):
            development = development + (development * 0.01 + 0.1)*(1-(development+0.0001)/10)

        return(development)

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

    def move_person(self, person, start, target):
        start.inhabitans.remove(person)
        target.inhabitans.append(person)
        person.location = []
        person.location.append(target)

    def return_population(self):
        return(len(self.inhabitans))

    def get_2nd_degree_neighbors(self):
        n2 = []
        for i in range(len(self.neighbors)):
            neighbor = self.neighbors[i]
            n2 = n2 + neighbor.neighbors
        n2 = list(set(n2))
        return(n2)


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
        for i in range(count):
            s = self.places[i]
            n = s.get_2nd_degree_neighbors()
            s.double_neighbors = n

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
