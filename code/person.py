from random import getrandbits, randint, choice, choices
from relation import isRelated, calcInbreeding

class person:
    def __init__(self):
        self.uid = None
        self.givenName = None
        self.surname = None
        self.isFemale = None
        self.doesReproduce = None #A general flag for any characters that for what ever reason don't reproduce

        self.race = None
        self.culture = None

        self.rank = None
        self.immunities = None
        self.plague = None
        self.inbreeding = 0 #How inbreed this person is from 0 to 1

        self.father = None
        self.mother = None
        self.parents = None
        self.isInbreed = False
        self.grandparents = []
        self.greatGrandparents = []

        self.spouse = None
        self.oldSpouses = []
        self.children = None
        self.pregnancyBreak = 0

        self.birthDate = None
        self.birthPlace = None
        self.deathDate = None
        self.deathPlace = None
        self.age = None
        self.isAlive = None
        self.currentPlace = None

    def setRandomSex(self):
        self.isFemale = bool(getrandbits(1))

    def setRandomDoesReproduce(self):
        if not self.race.doesReproduce:
            self.doesReproduce = False
        else:
            if randint(1, 20) == 1:
                self.doesReproduce = False
            else:
                self.doesReproduce = True

    def setRandomGivenName(self):
        self.givenName = self.culture.getRandomName(self.isFemale)

    def setRandomSurname(self):
        self.surname = self.culture.getRandomSurname()

    def determinRace(self, inputMotherRace, inputFatherRace):
        if inputMotherRace == inputFatherRace:
            outputRace = inputMotherRace
        else:
            try:
                outputRace = inputMotherRace.halfBreeds[inputFatherRace.name]
            except KeyError:
                outputRace = inputMotherRace

        return outputRace

    def setAncestors(self, inputMother, inputFather):
        self.parents = list()
        self.parents.extend([inputFather, inputMother])
        if inputFather.parents == None:
            fatherParents = list()
        else:
            fatherParents = inputFather.parents
        if inputMother.parents == None:
            motherParents = list()
        else:
            motherParents = inputMother.parents
        self.grandparents = fatherParents + motherParents
        self.greatGrandparents = inputFather.grandparents + inputMother.grandparents

    def createPerson(self, inputYear:int, inputUID:int, inputRace, inputCulture, inputAge:int, inputCurrentPlace, inputRank:int, inputOrigin):
        self.isAlive = True
        self.uid = inputUID
        self.setRandomSex()

        self.race = inputRace
        self.culture = inputCulture
        self.setRandomGivenName()
        self.setRandomSurname()
        self.setRandomDoesReproduce()

        self.birthDate = inputYear - inputAge
        self.age = inputAge

        self.birthPlace = inputOrigin
        self.currentPlace = inputCurrentPlace
        inputCurrentPlace.addPerson(self)

        if inputRank < 0:
            inputRank = 0
        self.rank = inputRank

    def birth(self, inputYear:int, inputUID:int, inputMother, inputFather):
        self.createPerson(inputYear, inputUID, self.determinRace(inputMother.race, inputFather.race), inputFather.culture, 0, inputMother.currentPlace, (inputFather.rank + randint(-1, 1)), inputMother.currentPlace.name)

        self.mother = inputMother
        inputMother.pregnancyBreak = inputMother.race.getRandomPregnancyBreak()
        self.father = inputFather
        self.setAncestors(inputMother, inputFather)
        if inputMother.children == None:
            inputMother.children = list()
        if inputFather.children == None:
            inputFather.children = list()

        if inputMother.immunities != None:
            for i in inputMother.immunities.keys():
                if randint(0, 100) <= 80:
                    if self.immunities == None:
                        self.immunities = dict()
                    self.immunities[i] = True
        inputMother.children.append(self)
        inputFather.children.append(self)
        self.inbreeding = calcInbreeding(self, 12)
        if isRelated(inputMother, inputFather, 3):
            self.isInbreed = True

        self.surname = inputFather.surname

    def death(self, inputYear:int):
        self.isAlive = False
        if self.spouse != None:
            self.spouse.currentPlace.updateUnmarried(self.spouse)
            self.spouse.spouse = None
            self.spouse = None

        self.deathPlace = self.currentPlace.name
        self.deathDate = inputYear
        self.currentPlace.removePerson(self)
        self.currentPlace = None

    def infect(self, inputPlague):
        if self.immunities == None or self.race.isImmune == False:
            self.plague = inputPlague
        else:
            if self.immunities[inputPlague.tag]:
                pass
            else:
                self.plague = inputPlague

    def spreadDisease(self):
        if (randint(0, 100) / 100) < self.plague.spreadChance:
            targets = list()
            if len(self.currentPlace.population) <= 20:
                spreadAmount = len(self.currentPlace.population)
            else:
                spreadAmount = int(len(self.currentPlace.population)/10)
            targets = choices(self.currentPlace.population, k=spreadAmount)
            for i in range(len(targets)):
                person = targets[i]
                if person.race.isImmune:
                    pass
                else:
                    person.infect(self.plague)

    def cure(self):
        if self.immunities == None:
            self.immunities = dict()
        self.immunities[self.plague.tag] = True
        self.plague == None

    def addOldSpouse(self, inputOldSpouse):
        self.oldSpouses.append(inputOldSpouse)
        self.oldSpouses = list(set(self.oldSpouses))
        inputOldSpouse.oldSpouses.append(self)
        inputOldSpouse.oldSpouses = list(set(inputOldSpouse.oldSpouses))

    def marry(self, inputPartner):
        self.spouse = inputPartner
        inputPartner.spouse = self
        self.addOldSpouse(inputPartner)


    def update(self):
        self.age +=1
        if self.plague != None:
            if self.plague.endurance < (randint(0, 100) / 100):
                self.cure()
            else:
                self.spreadDisease()
        if self.spouse != None:
            if self.spouse.isAlive == False:
                self.spouse = None
        if 0 < self.pregnancyBreak:
            self.pregnancyBreak -=1
