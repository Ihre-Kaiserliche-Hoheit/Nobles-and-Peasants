from random import choice

class location:
    def __init__(self):
        self.uid = None
        self.name = None
        self.X = None
        self.Y = None

        self.population = []
        self.populationCapacity = None

        self.hasHarbour = False

        self.unmarriedMale = []
        self.unmarriedFemale = []
        self.unmarriedAll = []

        self.neighbors = {}
        self.neighborIDs = []

    def create(self, inputEntry):
        self.uid = inputEntry["ID"]
        self.name = inputEntry["Name"]
        self.X = inputEntry["x"]
        self.Y = inputEntry["y"]

        self.populationCapacity = inputEntry["size"]

        self.neighborIDs = inputEntry["Neighbors"]

    def addPerson(self, inputPerson):
        inputPerson.currentPlace = self
        if inputPerson not in self.population:
            self.population.append(inputPerson)
            self.updateUnmarried(inputPerson)

    def removePerson(self, inputPerson):
        self.population.remove(inputPerson)

    def updateUnmarried(self, inputPerson):
        if inputPerson.race.adultAge <= inputPerson.age <= inputPerson.race.seniorAge and inputPerson.spouse == None:
            if inputPerson.isFemale and inputPerson not in self.unmarriedFemale:
                self.unmarriedFemale.append(inputPerson)
            elif inputPerson.isFemale == False and inputPerson not in self.unmarriedMale:
                self.unmarriedMale.append(inputPerson)
        try:
            if inputPerson.spouse.isAlive == False:
                inputPerson.spouse = None
        except AttributeError:
            pass

    def updateAll(self):
        queue = list()
        queue += self.population
        toRemove = list()
        for i in range(len(queue)):
            person = queue[i]
            if person.isAlive == False:
                toRemove.append(person)
                continue
            self.updateUnmarried(person)
        [self.removePerson(i) for i in toRemove]

    def updateUnmarriedInternal(self):
        unmarriedMale = list()
        unmarriedFemale = list()
        for i in range(len(self.unmarriedMale)):
            person = self.unmarriedMale[i]
            if (person.spouse == None or person.age <= person.race.seniorAge) and person.currentPlace == self:
                unmarriedMale.append(person)
        self.unmarriedMale = unmarriedMale
        for i in range(len(self.unmarriedFemale)):
            person = self.unmarriedFemale[i]
            if (person.spouse == None or person.age <= person.race.seniorAge) and person.currentPlace == self:
                unmarriedFemale.append(person)
        self.unmarriedFemale = unmarriedFemale
        self.unmarriedAll = unmarriedMale + unmarriedFemale

    def immigration(self, inputPerson, inputTarget):
        self.removePerson(inputPerson)
        inputTarget.addPerson(inputPerson)

    def findImmigrants(self):
        immigrants = list()

        for i in range(len(self.population)):
            person = self.population[i]
            if (person.children == None and person.spouse == None) or person.spouse == None or person.race.isImmortal:
                immigrants.append(person)

        for i in range(len(immigrants)):
            person = immigrants[i]
            target = self.neighbors[str(choice(self.neighborIDs))]
            tries = 0
            while target.populationCapacity < len(target.population) and tries < 6:
                target = self.neighbors[str(choice(self.neighborIDs))]
                tries +=1
            if target.populationCapacity < len(target.population):
                self.immigration(person, target)
