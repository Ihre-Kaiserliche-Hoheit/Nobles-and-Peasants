from random import randint


class race():
    def __init__(self):
        self.name = ""

        self.life_expectancy = 80 #How old members of this race can get on average
        self.child = 10 #How old members of the race needs to be considered a teen
        self.adult = 21 #How old members of the race needs to be considered a adult
        self.old = 50 #How old members of the race needs to be considered old
        self.ancient = 90 #How old members of the race needs to be considered ancient

        self.pregnancy_challenge = 6 #D20, How hard it is to get pregnant
        self.child_death_challenge = 1 #D20, How likly a child will die during the first year of life
        self.pregnancy_break_minimum = 1
        self.pregnancy_break_maximum = 4

        self.isHalf = False #Is the race a half breed race?
        self.isDominant = False #Does this race overwrite the gene expresion of other races, ie Tiefling
        self.canBreed = True #Do members of this race reproduce on their own, ie Humans = True, Warforged = False
        self.canInterbreed = True #Can members of this race breed with members of other breed groups?
        self.isNative = False
        self.cultures = []
        self.breed_group = "" #Humans are concidered breed_group = "all",
        """
        Certain races can only breed with other closly related races, this is how they are indenified.
        For example if only Trolls and Ogres can breed with each other but not with, for example humans, they would be in
        their own group.
        Needs canBreed to be True, if two races of two different breed groups want to breed they both need canInterbreed = True
        """
        self.half_breeds = { #List of all the half breeds the race can produce
        }

    def create(self, _input):
        self.name = _input["tag"]

        self.life_expectancy = _input["life_expectancy"]
        self.child = _input["child"]
        self.adult = _input["adult"]
        self.old = _input["old"]
        self.ancient = _input["ancient"]

        self.pregnancy_challenge = _input["pregnancy_challenge"]
        self.child_death_challenge = _input["child_death_challenge"]
        self.pregnancy_break_minimum = _input["pregnancy_break_minimum"]
        self.pregnancy_break_maximum = _input["pregnancy_break_maximum"]

        self.isHalf = _input["isHalf"]
        self.isDominant = _input["isDominant"]
        self.canBreed = _input["canBreed"]
        self.canInterbreed = _input["canInterbreed"]
        self.breed_group = _input["breed_group"]
        self.isNative = _input["isNative"]
        self.cultures = _input["cultures"]
        self.half_breeds = _input["half_breeds"]

    def random_age(self, _range:str="adult"):
        result = 0
        if _range == "young":
            result = randint(0, self.adult)
        elif _range == "adult":
            result = randint(self.adult, self.old)
        elif _range == "old":
            result = randint(self.old, self.life_expectancy)
        elif _range == "ancient":
            result = randint(self.life_expectancy, self.ancient)
        return(result)

    def isCompatible(self, _other_race):
        if (self.canInterbreed and _other_race.canInterbreed and
            self.canBreed and _other_race.canBreed and
            _other_race.breed_group == self.breed_group):
                    return True
        else:
            return False

    def get_half_breed(self, _other_race_tag:str):
        half = self.half_breeds[_other_race_tag]
        return half
