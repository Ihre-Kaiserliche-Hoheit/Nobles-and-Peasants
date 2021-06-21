from random import choice

class culture():
    def __init__(self):
        self.name = ""

        self.male_names = []
        self.female_names = []
        self.surnames = []

        self.noble_prefix = ""
        self.patronym_son = ""
        self.patronym_daughter = ""

        self.isPatriach = True
        self.hasPatronym = False
        self.hasSurname = True

    def return_random_name(self, _isFemale):
        if _isFemale == True:
            return(choice(self.female_names))
        else:
            return(choice(self.male_names))

    def return_random_surname(self):
        return(choice(self.surnames))

    def create(self, _input):
        self.name = _input["name"]
        self.male_names = _input["male"]
        self.female_names = _input["female"]
        self.surnames = _input["surname"]

        self.noble_prefix = _input["noble_prefix"]
        self.patronym_son = _input["patronym_son"]
        self.patronym_daughter = _input["patronym_daughter"]

        self.isPatriach = _input["isPatriach"]
        self.hasPatronym = _input["hasPatronym"]
        self.hasSurname = _input["hasSurname"]
