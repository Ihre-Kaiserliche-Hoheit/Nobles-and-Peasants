class plague():
    def __init__(self):
        self.tag = ""
        self.name = ""
        self.deadliness = 0
        self.endurance = 0
        self.spreadChance = 0

    def create(self, inputEntry):
        self.tag = inputEntry["tag"]
        self.name = inputEntry["name"]
        self.deadliness = inputEntry["deadliness"]
        self.endurance = inputEntry["endurance"]
        self.spreadChance = inputEntry["spreadChance"]
