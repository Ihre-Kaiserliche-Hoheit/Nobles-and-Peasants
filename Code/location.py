from random import randint, choice
from internal_lib import randlist

class location():
    def __init__(self):
        self.uid = None
        self.name = ""

        self.size = 0
        self.x = 0
        self.y = 0

        self.hasPlague = False
        self.hadPlague = False
        self.plague = None
        self.plagueCooldown = 0
        self.plagueLength = 0
        self.immuneTo = dict()

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

    def update(self, _year, _plagues, _plague_tags):
        if 0 < len(self.inhabitans):
            self.update_inhabitans()
            self.update_free_lists()
            self.plagueUpdate(_year, _plagues, _plague_tags)
            if int(self.size*1.25) < len(self.inhabitans):
                self.cull_population(_year, int(len(self.inhabitans)*0.1))
        else:
            self.hadPlague = False
            self.hasPlague = False
            self.plague = None
            self.plagueCooldown = 0
            self.plagueLength = 0
            self.immuneTo = dict()

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
                if self.plague.tag not in self.immuneTo and victim.race.immune == False:
                    victim.death(_year)
            else:
                if victim.race.immortal == False:
                    victim.death(_year)

    def spreadPlague(self, _plagues):
        for i in range(len(self.neighbors)):
            neighbor = self.neighbors[i]
            neighbor.infect(_plagues, self.plague.tag)

    def plagueUpdate(self, _year, _plagues, _plague_tags):
        if self.hasPlague:
            death_count = int(len(self.inhabitans)*self.plague.deadliness)
            self.cull_population(_year, death_count, "plague")
            self.spreadPlague(_plagues)
            self.plagueLength -=1
            if self.plagueLength == 0:
                self.cure(_year)
        else:
            newImmuneTo = dict()
            for plague, year in self.immuneTo.items():
                if year < _year+40:
                    newImmuneTo[plague] = year
            self.immuneTo = newImmuneTo
            if self.plagueCooldown == 0:
                if int(self.size*1.2) < len(self.inhabitans):
                    if randint(0, 10) == 10:
                        self.infect(_plagues, choice(_plague_tags))
            else:
                self.plagueCooldown -=1

    def cure(self, _year):
        self.immuneTo[self.plague.tag] = _year
        self.hasPlague = False
        self.hadPlague = False
        self.plagueCooldown = 3
        self.plague = None

    def infect(self, _plagues, _plague_tag):
        self.hasPlague = True
        self.plague = _plagues[_plague_tag]
        self.plagueLength = 0
        self.plagueLength += self.plague.endurance
