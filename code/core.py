from person import person
from location import location
from culture import culture
from race import race
import modifier as mod
from plague import plague
import seedGen as sg
from relation import getAncestors, calcInbreeding, isSibling
from json_exporter import convertData

import json as j
import random as r
from random import randint, choice, getrandbits, choices


#TODO add inherited immunity


class world:
    def __init__(self):
        self.startYear = None
        self.endYears = None
        self.doPrint = None
        self.autoViewer = None

        self.Seed = None
        self.Date = sg.get_time()

        self.totalPopulation = list()
        self.livingPopulation = 0
        self.locations = []

        self.cultureTags = []
        self.cultures = {}

        self.raceTags = []
        self.races = {}

        self.plagueTags = []
        self.plagues = {}

        self.year = None
        self.population = 0
        self.events = {}

        self.create()

    def setSeed(self, inputSeed=None):
        if inputSeed == None:
            self.Seed = sg.pseudo_random_seed()
            self.Seed = sg.convert_to_hash(self.Seed, 16)
        else:
            self.Seed = inputSeed
        self.Seed = str(self.Seed)
        if self.doPrint == True: print("RNG Seed: "+str(self.Seed) + " | Start Setup...")
        Hash_Seed = sg.convert_to_hash(self.Seed, 16) #Converts the input into a has with the length of 16
        r.seed(Hash_Seed)

    def readSettings(self):
        with open("../input/settings.json") as settings:
            settings = j.load(settings)
        #If it is still shitty you may want to sacrifice a goat or two to appease the machine spirit
        self.doPrint = settings["printOutput"]
        self.autoViewer = settings["autoStartViewer"]

        self.startYear = settings["startYear"]
        self.endYear = settings["endYear"]
        self.year = self.startYear

        self.setSeed(settings["seed"])

    def createRaces(self):
        with open("../input/races.json") as races:
            races = j.load(races)
        races = races["races"]
        self.raceTags = races["header"]
        for raceTag in self.raceTags:
            self.createRace(races, raceTag)

    def createRace(self, inputRaces, inputRaceTag):
        newRace = race()
        newRace.create(inputRaces[inputRaceTag])
        self.races[inputRaceTag] = newRace

    def createCultures(self):
        with open("../input/cultures.json") as cultures:
            cultures = j.load(cultures)
        self.cultureTags = cultures["header"]
        for cultureTag in self.cultureTags:
            self.createCulture(cultures, cultureTag)

    def createCulture(self, inputCulutres, inputCultureTag):
        newCulture = culture()
        newCulture.create(inputCulutres[inputCultureTag])
        self.cultures[inputCultureTag] = newCulture

    def createPlagues(self):
        with open("../input/plague.json") as plagues:
            plagues = j.load(plagues)
        self.plagueTags = plagues["plagues"]
        for plagueTag in self.plagueTags:
            self.createPlague(plagues, plagueTag)

    def createPlague(self, inputPlagues, inputPlagueTag):
        newPlague = plague()
        newPlague.create(inputPlagues[inputPlagueTag])
        self.plagues[inputPlagueTag] = newPlague

    def createLocations(self):
        with open("../input/world.json") as locations:
            locations = j.load(locations)
        for i in range(len(locations)):
            self.createLocation(locations[i])
        for i in range(len(self.locations)):
            location = self.locations[i]
            for ii in range(len(location.neighborIDs)):
                neigborID = location.neighborIDs[ii]
                neigbor = self.locations[neigborID]
                location.neighbors[str(neigbor.uid)] = neigbor

    def createLocation(self, inputLocationEntry):
        newLocation = location()
        newLocation.create(inputLocationEntry)
        self.locations.append(newLocation)

    def create(self):
        self.readSettings()
        self.createRaces()
        self.createCultures()
        self.createLocations()
        self.createPlagues()
        self.eventReadAll()

    def createRandomPerson(self, inputLocation, inputRank:int, inputOrigin):
        newPerson = person()
        race = self.races[choice(self.raceTags)]
        newPerson.createPerson(self.year, len(self.totalPopulation), race, self.cultures[choice(self.cultureTags)], randint(race.adultAge, int(race.seniorAge*0.8)), inputLocation, inputRank, inputOrigin)
        self.totalPopulation.append(newPerson)
        inputLocation.addPerson(newPerson)

    def createRandomGroup(self, inputLocation:int, inputRank:int, inputCount:int, inputOrigin:str="New World"):
        location = self.locations[inputLocation]
        for i in range(inputCount):
            self.createRandomPerson(location, inputRank, inputOrigin)

    def createPerson(self, inputLocation, inputRace, inputCulture, inputRank:int, inputOrigin):
        newPerson = person()
        newPerson.createPerson(self.year, len(self.totalPopulation), inputRace, inputCulture, randint(inputRace.adultAge, int(inputRace.seniorAge*0.8)), inputLocation, inputRank, inputOrigin)
        self.totalPopulation.append(newPerson)
        inputLocation.addPerson(newPerson)

    def createGroup(self, inputLocation, inputRace, inputCulture, inputRank:int, inputCount:int, inputOrigin):
        for i in range(inputCount):
            self.createPerson(inputLocation, self.races[inputRace], self.cultures[inputCulture], inputRank, inputOrigin)

    def eventPlague(self, inputLocation, inputPlague):
        infectet = choices(inputLocation.population, k=int(len(inputLocation.population) / 10))
        for sick in infectet:
            sick.infect(self.plagues[inputPlague])

    def eventImmigration(self, inputLocation, inputRace, inputCulture, inputRank, inputSize, inputOrigin:str="Old World"):
        self.createGroup(inputLocation, inputRace, inputCulture, inputRank, inputSize, inputOrigin)

    def eventReadAll(self):
        with open("../input/events.json") as events:
            events = j.load(events)
        self.events = events["events"]
        pass

    def eventManager(self, inputEvents):
        for i in range(len(inputEvents)):
            event = inputEvents[i]
            if event["type"] == "plague":
                self.eventPlague(self.locations[event["location"]], event["plague"])
            if event["type"] == "immigration":
                self.eventImmigration(self.locations[event["location"]], event["race"], event["culture"], event["rank"], event["size"], event["origin"])

    def marriage(self, inputSearcher):
        viablePartners = list()
        partner = None
        if inputSearcher.isFemale and len(inputSearcher.currentPlace.unmarriedMale) != 0:
            viablePartners = choices(inputSearcher.currentPlace.unmarriedMale, k=round(len(inputSearcher.currentPlace.unmarriedMale)/2))
        elif inputSearcher.isFemale == False and len(inputSearcher.currentPlace.unmarriedFemale) != 0:
            viablePartners = choices(inputSearcher.currentPlace.unmarriedFemale, k=round(len(inputSearcher.currentPlace.unmarriedFemale)/2))
        if len(viablePartners) != 0:
            for i in range(len(viablePartners)):
                if partner == None:
                    viablePartner = viablePartners[i]
                    if  (viablePartner.doesReproduce and viablePartner.isAlive and isSibling(inputSearcher, viablePartner) == False and
                        (inputSearcher.race == viablePartner.race or (viablePartner.race.canInterbreed and inputSearcher.race.canInterbreed)) and
                        (viablePartner.spouse == None)):
                        chance = 0.2
                        chance += mod.modifierMarriage(inputSearcher, viablePartner)
                        roll = randint(0, 100) / 100
                        if chance < roll:
                            partner = viablePartner
        if partner != None:
            inputSearcher.marry(partner)

            if partner.isFemale and partner in partner.currentPlace.unmarriedFemale:
                partner.currentPlace.unmarriedFemale.remove(partner)
                #inputSearcher.currentPlace.unmarriedMale.remove(inputSearcher)
            elif partner.isFemale == False and partner in partner.currentPlace.unmarriedMale:
                partner.currentPlace.unmarriedMale.remove(partner)
                #inputSearcher.currentPlace.unmarriedFemale.remove(inputSearcher)

    def death(self, inputPerson):
        inputPerson.death(self.year)

    def birth(self, inputMother, inputFather):
        newborn = person()
        newborn.birth(self.year, len(self.totalPopulation), inputMother, inputFather)
        self.totalPopulation.append(newborn)
        if (randint(0, 100) / 100) < (newborn.race.childMortality + newborn.inbreeding):
            self.death(newborn)

    def update(self):
        self.year += 1
        self.livingPopulation = 0
        if str(self.year) in self.events:
            self.eventManager(self.events[str(self.year)])
        for i in range(len(self.locations)):
            currentLocation = self.locations[i]

            if len(currentLocation.population) == 0:
                continue
            if int(currentLocation.populationCapacity*0.8) < len(currentLocation.population):
                roll = randint(1, 10)
                if 3 <= roll < 7:
                    currentLocation.findImmigrants()

                if round(currentLocation.populationCapacity*1.3, 0) < len(currentLocation.population):
                    if 2 <= roll < 3:
                        self.eventManager([{"type":"plague", "location":currentLocation.uid, "plague":"old_pox"}])

            queue = list()
            queue += currentLocation.population
            currentLocation.updateAll()
            self.livingPopulation += len(currentLocation.population)
            for ii in range(len(queue)):
                currentPerson = queue[ii]
                currentPerson.update()
                if currentPerson.race.seniorAge <= currentPerson.age or currentPerson.plague != None or 0.5 < currentPerson.inbreeding:
                    chance = 0.02
                    chance += mod.modifierDeath(currentPerson)
                    roll = randint(0, 100) / 100
                    if roll < chance:
                        self.death(currentPerson)
                        continue
                if currentPerson.spouse == None and currentPerson.doesReproduce:
                    self.marriage(currentPerson)
                if currentPerson.isFemale and currentPerson.age < currentPerson.race.seniorAge:
                    if currentPerson.spouse != None:
                        if currentPerson.spouse.isAlive and currentPerson.pregnancyBreak <= 0:
                            if (randint(0, 100) / 100) < currentPerson.race.pregnancyChance:
                                self.birth(currentPerson, currentPerson.spouse)
                        #Check if current spouse is alive goes here
            currentLocation.updateUnmarriedInternal()

w = world()
w.eventManager(w.events["start"])
print(vars(w.totalPopulation[0]))
for i in range(w.startYear, w.endYear):
    w.update()
    print(str(w.year) +" : "+str(w.livingPopulation))
convertData(w.totalPopulation, w.Seed, w.doPrint)
