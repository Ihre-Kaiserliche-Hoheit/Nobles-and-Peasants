from random import getrandbits, randint


class person():
    def __init__(self):
        self.uid = None
        self.name = ""
        self.patronym = ""
        self.surname = ""
        self.isFemale = None
        self.culture = None
        self.race = None
        self.relations = {
        "father":None,
        "mother":None,
        "spouse":None,
        "children":None,

        "parents":None,
        "grandparents":[],
        "great grandparents":[]
        }
        self.post_pregnancy = 0
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
        _mother.post_pregnancy = randint(1, 3)
        #Set ancestors
        self.relations["father"] = _father
        self.relations["mother"] = _mother
        self.relations["parents"] = [self.relations["father"]] + [self.relations["mother"]]
        if _father.relations["parents"] == None and _mother.relations["parents"] == None:
            pass
        elif _mother.relations["parents"] == None:
            self.relations["grandparents"] = _father.relations["parents"]
        elif _father.relations["parents"] == None:
            self.relations["grandparents"] = _mother.relations["parents"]
        else:
            self.relations["grandparents"] = _father.relations["parents"] + _mother.relations["parents"]
        self.relations["great grandparents"] = _father.relations["grandparents"] + _mother.relations["grandparents"]

        if _mother.relations["children"] == None:
            _mother.relations["children"] = list()
        if _father.relations["children"] == None:
            _father.relations["children"] = list()
        _mother.relations["children"].append(self)
        _father.relations["children"].append(self)
        self.current_location = _mother.current_location
        self.birth_location = self.current_location.name
        self.current_location.add_person(self)
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
        self.current_location.remove_person(self)
        self.current_location = None

    def add_spouse(self, _spouse):
        self.relations["spouse"] = _spouse

    def update(self):
        self.age += 1
