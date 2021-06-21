from random import getrandbits


class person():
    def __init__(self):
        self.uid = None
        self.name = ""
        self.patronym = ""
        self.surname = ""
        self.isFemale = None
        self.culture = None
        self.relations = {
        "father":None,
        "mother":None,
        "spouse":None,
        "children":None,

        "parents":[],
        "grandparents":[],
        "great grandparents":[]
        }
        self.birth_date = None
        self.birth_location = None
        self.age = 0
        self.current_location = None
        self.death_date = None
        self.death_location = None

        self.isAlive = True

    def set_random_sex(self):
        self.isFemale = bool(getrandbits(1))

    def birth(self, _year, _father, _mother):
        #Only does the most basic stuff
        self.set_random_sex()
        self.birth_date = _year
        self.relations["father"] = _father
        self.relations["mother"] = _mother
        self.relations["parents"] = self.relations["father"] + self.relations["mother"]
        self.relations["grandparents"] = _father.relations["parents"] + _mother.relations["parents"]
        self.relations["great grandparents"] = _father.relations["grandparents"] + _mother.relations["grandparents"]

        self.current_location = _mother.current_location
        self.birth_location = self.current_location.name
        self.set_culture()

    def set_culture(self):
        mother = self.relations["mother"]
        if mother.culture.isPatriach == False:
            self.culture = mother.culture
        else:
            father = self.relations["father"]
            self.culture = father.culture

    def death(self, _year):
        self.death_date = _year
        self.death_location = self.current_location.name
        self.isAlive = False
