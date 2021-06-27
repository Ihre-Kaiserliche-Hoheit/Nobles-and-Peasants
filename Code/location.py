from internal_lib import create_random_list_from as randlist
from random import randint

class location():
    def __init__(self):
        self.uid = None
        self.name = ""

        self.size = 0
        self.x = 0
        self.y = 0

        self.hasPlague = False
        self.hadPlague = False
        self.PlagueCount = 0

        self.inhabitans = []
        self.free_males = []
        self.free_females = []

        self.neighbors = [] #Links to all neighbors
        self.neighbor_uids = [] #UIDs of all neighbors

    def create(self, _input):
        self.uid = _input["ID"]
        self.name = _input["Name"]

        self.size = _input["size"]
        self.x = _input["x"]
        self.y = _input["y"]

        self.neighbor_uids = _input["Neighbors"]

    def update_free_lists(self):
        all = self.inhabitans
        free_males = list()
        free_females = list()
        for i in range(len(all)):
            person = all[i]
            if person.relations["spouse"] == None and person.race.adult < person.age < person.race.old and person.doesReproduce:
                if person.isFemale == False:
                    free_males.append(person)
                else:
                    free_females.append(person)
        self.free_males = free_males
        self.free_females = free_females

    def update_inhabitans(self):
        all = self.inhabitans
        new_inhabitans = list()
        for i in range(len(all)):
            person = all[i]
            if person.isAlive == True:
                new_inhabitans.append(person)
        self.inhabitans = new_inhabitans

    def add_person(self, _person):
        self.inhabitans.append(_person)
        _person.current_location = self

    def remove_person(self, _person):
        try:
            self.inhabitans.remove(_person)
        except ValueError:
            pass

    def update(self, _year):
        if 0 < len(self.inhabitans):
            self.update_inhabitans()
            self.update_free_lists()
            if int(self.size*1.25) < len(self.inhabitans):
                self.cull_population(_year, int(len(self.inhabitans)*0.1))
            if int(self.size*1.2) < len(self.inhabitans):
                if randint(0, 10) == 10:
                    self.hasPlague = True
            if self.hasPlague:
                self.spreadPlague()
                self.plagueUpdate(_year)
            elif self.hadPlague and 0 < self.PlagueCount:
                self.PlagueCount -=1
        else:
            self.hadPlague = False
            self.hasPlague = False
            self.PlagueCount = 0

    def migrate(self, _person, _target):
        self.remove_person(_person)
        _target.add_person(_person)

    def cull_overpopulation(self, _year):
        victims = randlist(self.inhabitans, )
        for i in range(len(victims)):
            victim = victims[i]
            if victim.current_location == None:
                victim.current_location = self
            victim.death(_year)

    def cull_population(self, _year, _amount:int, _cause:str="default"):
        victims = randlist(self.inhabitans, _amount)
        for i in range(len(victims)):
            victim = victims[i]
            if victim.current_location == None:
                victim.current_location = self
            if _cause == "plague":
                if victim.race.isNative or 500 < _year:
                    victim.death(_year)
            else:
                victim.death(_year)

    def spreadPlague(self):
        neighbors = self.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor.hadPlague == False and len(neighbor.inhabitans) != 0:
                neighbor.infect()

    def plagueUpdate(self, _year):
        self.cull_population(_year, int((len(self.inhabitans)*0.5)), "plague")
        self.hasPlague = False
        self.hadPlague = True

    def infect(self):
        self.hasPlague = True
        self.PlagueCount = 2
