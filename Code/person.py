from random import getrandbits, randint, choice


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
        self.doesReproduce = True

    def set_random_sex(self):
        self.isFemale = bool(getrandbits(1))

    def set_doesReproduce(self):
        if 9 < randint(0, 10):
            self.doesReproduce = False

    def birth(self, _year, _father, _mother):
        #Only does the most basic stuff
        self.set_random_sex()
        self.set_doesReproduce()
        self.birth_date = _year
        _mother.post_pregnancy = randint(_mother.race.pregnancy_break_minimum, _mother.race.pregnancy_break_maximum)
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
        self.set_name()

    def set_name(self):
        self.name = self.culture.return_random_name(self.isFemale)
        if self.culture.isPatriach:
            parent = self.relations["father"]
        else:
            parent = self.relations["mother"]
        if self.culture.hasPatronym:
            if self.isFemale:
                suffix = self.culture.patronym_daughter
            else:
                suffix = self.culture.patronym_son
            self.patronym = parent.name + suffix
        if self.culture.hasSurname:
            if parent.surname != "":
                self.surname = parent.surname
            else:
                self.surname = self.race.return_random_surname()

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
