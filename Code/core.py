print("Starting...") #Shows that it is alive

#Imports
from person import person
from culture import culture
from location import location
from race import race
from dice import roll
from modifiers import death_modifiers, child_mortality_modifiers
import relation as re

import internal_lib as il
import json as j
import math as m
import random as r


#Variables
##Settings
with open("../Input/settings.json") as settings:
    settings = j.load(settings)

start_year = settings["start_year"]
end_year = settings["end_year"]
doPrint = settings["print_output"]

Seed = None
if settings["seed"] == None:
    Seed = il.pseudo_random_seed()
else:
    Seed = settings["seed"]
if doPrint == True: print("RNG Seed: "+str(Seed) + " | Start Setup...")
Seed = il.convert_to_hash(Seed, 16) #Converts the input into a has with the length of 16
r.seed(Seed)
##Globals
total_population = []
locations = []
cultures = {}
races = {}
year = start_year
population = settings["start_population"]

#Functions
def create_cultures():
    with open("../Input/cultures.json") as culturess:
        culturess = j.load(culturess)
    culture_header = culturess["header"]
    culture_tags = culture_header["culture_list"]
    for i in range(len(culture_tags)):
        culture_tag = culture_tags[i]
        culture_entry = culturess[culture_tag]
        create_culture(culture_entry, culture_tag)

def create_culture(_entry, _tag):
    new_culture = culture()
    new_culture.create(_entry)
    cultures[_tag] = new_culture

def create_locations():
    with open("../Input/world.json") as world:
        world = j.load(world)
    world = world["settlements"]
    #Creates locations
    for i in range(len(world)):
        location_entry = world[i]
        create_location(location_entry)
    #Connects locations
    for i in range(len(locations)):
        entry = locations[i]
        for ii in range(len(entry.neighbor_uids)):
            entry_secundus_uid = entry.neighbor_uids[ii]
            entry_secundus = locations[entry_secundus_uid]
            entry.neighbors.append(entry_secundus)

def create_location(_entry):
    new_location = location()
    new_location.create(_entry)
    locations.append(new_location)

def create_races():
    with open("../Input/races.json") as races_input:
        races_input = j.load(races_input)
    races_input = races_input["races"]
    race_header = races_input["header"]
    for i in range(len(race_header)):
        race_tag = race_header[i]
        race_entry = races_input[race_tag]
        create_race(race_entry, race_tag)

def create_race(_entry, _tag):
    new_race = race()
    new_race.create(_entry)
    races[_tag] = new_race

def create_all(): #Creates cultures, races and locations
    create_cultures()
    create_locations()
    create_races()

def add_to_population(_person):
    total_population.append(_person)

def create_start_population(_size:int, _race:str, _culture:str, _location:int=0, _birth_location:str="Old World"):
    for i in range(_size):
        race = races[_race]
        create_person(_race, _culture, _location, _birth_location, race.random_age("adult"))

def create_person(_race:str, _culture:str, _location:int=0, _birth_location:str="Old World", _age:int=20):
    new_person = person()
    new_person.uid = len(total_population)
    new_person.set_random_sex()
    new_person.race = races[_race]
    new_person.culture = cultures[_culture]
    new_person.name = new_person.culture.return_random_name(new_person.isFemale)
    new_person.surname = new_person.culture.return_random_surname()
    new_person.current_location = locations[_location]
    new_person.current_location.add_person(new_person)
    new_person.age = _age
    new_person.birth_date = year - _age
    new_person.birth_location = _birth_location
    add_to_population(new_person)

def marriage(_person, _location):
    viable = list()
    possible = list()
    if _person.isFemale == True:
        possible = _location.free_males
    else:
        possible = _location.free_females

    for i in range(len(possible)):
        person2 = possible[i]
        if re.is_related(_person, person2, 4) == False:
            viable.append(person2)
    try:
        spouse = r.choice(viable)
        check = roll()
        if 8 < check:
            _person.add_spouse(spouse)
            spouse.add_spouse(_person)
    except IndexError:
        pass

def birth(_mother, _father):
    child = person()
    child.birth(year, _father, _mother)
    child.race = determin_race(child)
    add_to_population(child)
    check = roll()
    if check < (child.race.child_death_challenge + child_mortality_modifiers(child)):
        death(child)

def determin_race(_person):
    father = _person.relations["father"]
    mother = _person.relations["mother"]
    if father.race == mother.race:
        return father.race
    elif father.race.isCompatible(mother.race):
        half = mother.race.get_half_breed(father.race.name)
        return races[half]

def findMigrationTarget(_start_location):
    targets = list()
    targets += _start_location.neighbors
    r.shuffle(targets)
    for i in range(len(targets)):
        target = targets[i]
        if len(target.inhabitans) < int(target.size*1.1):
            return target
    return None


def doMigrate(_person):
    if _person.current_location.size < (len(_person.current_location.inhabitans)*0.9):
        target = findMigrationTarget(_person.current_location)
        if target != None:
            if _person in _person.current_location.free_females:
                _person.current_location.migrate(_person, target)
            elif  _person in _person.current_location.free_males:
                _person.current_location.migrate(_person, target)

def death(_person):
    _person.death(year)

def update():
    population = 0
    for i in range(len(locations)):
        place = locations[i]
        place.update(year)
    for i in range(len(locations)):
        place = locations[i]
        if len(place.inhabitans) != 0:
            inhabitans = place.inhabitans
            queue = list()
            queue += place.inhabitans
            for ii in range(len(queue)):
                dude = queue[ii]
                dude.update()
                if dude.relations["spouse"] != None:
                    if dude.isFemale == True and dude.race.adult <= dude.age <= dude.race.old:
                        if 0 < dude.post_pregnancy:
                            dude.post_pregnancy -=1
                        elif dude.post_pregnancy == 0:
                            check = roll()
                            spouse = dude.relations["spouse"]
                            if dude.race.isCompatible(spouse.race) and dude.race.pregnancy_challenge < check and spouse.isAlive == True:
                                birth(dude, spouse)
                else:
                    marriage(dude, dude.current_location)
                doMigrate(dude)
                if dude.race.old < dude.age:
                    check = roll(_mods=(dude.race.life_expectancy / dude.age))
                    challenge = 10 + death_modifiers(dude)
                    if challenge < check:
                        death(dude)

        population += len(inhabitans)
    if doPrint == True: print("Year: "+str(year)+" | Population: "+str(population))

#Running code
create_all()
if doPrint == True: print("Setup: Part I - Finished")
create_start_population(settings["start_population"], "Human", "template")
if doPrint == True: print("Setup: Part II - Finished")

for i in range(start_year, end_year+1):
    year = i
    update()
print("...Finished")
