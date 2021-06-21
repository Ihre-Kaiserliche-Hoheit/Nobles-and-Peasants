class race():
    def __init__(self):
        self.name = ""

        self.life_expactancy = 80 #How old members of this race can get on average

        self.pregnancy_challenge = 10 #D20, How hard it is to get pregnant
        self.child_death_challenge = 1 #D20, How likly a child will die

        self.isHalf = False #Is the race a half breed race?
        self.isDominant = False #Does this race overwrite the gene expresion of other races, ie Tiefling
        self.canBreed = True #Do members of this race reproduce on their own, ie Humans = True, Warforged = False
        self.canInterbreed = True #Can members of this race breed with members of other breed groups?
        self.breed_group = "" #Humans are concidered breed_group = "all",
        """
        Certain races can only breed with other closly related races, this is how they are indenified.
        For example if only Trolls and Ogres can breed with each other but not with, for example humans, they would be in
        their own group.
        Needs canBreed to be True, if two races of two different breed groups want to breed they both need canInterbreed = True
        """
        self.half_breeds = { #List of all the half breeds the race can produce
            "elf":"half-elf"
        }

    def create(self, _input):
        self.name = _input["tag"]

        self.life_expactancy = _input["life_expectancy"]

        self.pregnancy_challenge = _input["pregnancy_challenge"]
        self.child_death_challenge = _input["child_death_challenge"]

        self.isHalf = _input["isHalf"]
        self.isDominant = _input["isDominant"]
        self.canBreed = _input["canBreed"]
        self.canInterbreed = _input["canInterbreed"]
        self.breed_group = _input["breed_group"]

        self.half_breeds = _input["half_breeds"]
