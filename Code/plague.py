class plague():
    def __init__(self):
        self.tag = ""
        self.name = ""
        self.deadliness = 0
        self.endurance = 0
        self.spread_chance = 0

    def create(self, _entry):
        self.tag = _entry["tag"]
        self.name = _entry["name"]
        self.deadliness = _entry["deadliness"]
        self.endurance = _entry["endurance"]
        self.spread_chance = _entry["spread_chance"]
