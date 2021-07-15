from random import choice

class culture:
    def __inti__(self):
        self.name = None

        self.maleNames = []
        self.femaleNames = []
        self.surnames = []

    def getRandomName(self, inputIsFemale):
        if inputIsFemale:
            return choice(self.femaleNames)
        else:
            return choice(self.maleNames)

    def getRandomSurname(self):
        return choice(self.surnames)

    def create(self, inputEntry):
        self.name = inputEntry["name"]

        self.maleNames = inputEntry["male"]
        self.femaleNames = inputEntry["female"]
        self.surnames = inputEntry["surnames"]
