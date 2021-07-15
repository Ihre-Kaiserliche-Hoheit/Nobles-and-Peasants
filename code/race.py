from random import randint

class race:
    def __init__(self):
        self.name = None

        self.averageLifeExpectancy = None
        self.teenAge = None #At what age they are considered a teenager
        self.adultAge = None #At what age they are considered an adult
        self.seniorAge = None #At what age they are considered a old and unable to do heavy labour

        self.isImmune = None #Are they immune to all common diseases?
        self.isImmortal = None #Are they immune to age?

        self.pregnancyChance = None #How likly they are to get pregnant after intercourse from 0 to 1
        self.childMortality = None
        self.doesReproduce = None #Do they reproduce like normal organics?
        self.canInterbreed = None #Can they breed with people from other races?

        self.minimumPregnancyBreak = 0
        self.maximumPregnancyBreak = 0

        self.halfBreeds = None #List of half breeds this race can prodcue, only needed if they can interbreed

    def create(self, inputEntry):
        self.name = inputEntry["name"]

        self.averageLifeExpectancy = inputEntry["averageLifeExpectancy"]
        self.teenAge = inputEntry["teenAge"]
        self.adultAge = inputEntry["adultAge"]
        self.seniorAge = inputEntry["seniorAge"]

        self.isImmune = inputEntry["isImmune"]
        self.isImmortal =inputEntry["isImmortal"]

        self.pregnancyChance = inputEntry["pregnancyChance"]
        self.childMortality = inputEntry["childDeathChance"]
        self.doesReproduce = inputEntry["doesReproduce"]
        self.canInterbreed = inputEntry["canInterbreed"]

        self.minimumPregnancyBreak = inputEntry["pregnancy_break_minimum"]
        self.maximumPregnancyBreak = inputEntry["pregnancy_break_maximum"]

        self.halfBreeds = inputEntry["halfBreeds"]

    def getRandomPregnancyBreak(self):
        return randint(self.minimumPregnancyBreak, self.maximumPregnancyBreak)
