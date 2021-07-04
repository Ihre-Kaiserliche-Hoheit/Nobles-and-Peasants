print("Starting...") #Shows that it is alive

#Imports
from modifiers import death_modifiers, child_mortality_modifiers
from internal_lib import randlist
import relation as re

from person import person
from location import location
from race import race
from plague import plague
from culture import culture
import json_exporter as jex

import internal_lib as il
import json as j
import math as m
import random as r
from random import getrandbits, randint, choice


#Variables
##Settings
with open("../Input/settings.json") as settings:
    settings = j.load(settings)

start_year = settings["start_year"]
end_year = settings["end_year"]
doPrint = settings["print_output"]
auto_viewer = settings["auto_start_viewer"]

Seed = None
Date = il.get_time()
if settings["seed"] == None:
    Seed = il.pseudo_random_seed()
    Seed = il.convert_to_hash(Seed, 16)
else:
    Seed = settings["seed"]
Seed = str(Seed)
if doPrint == True: print("RNG Seed: "+str(Seed) + " | Start Setup...")
Hash_Seed = il.convert_to_hash(Seed, 16) #Converts the input into a has with the length of 16
r.seed(Hash_Seed)
##Globals
total_population = list()
locations = []

culture_tags = []
cultures = {}

race_tags = []
races = {}

plague_tags = []
plagues = {}

year = start_year
population = 0
events = {}

#Functions
def create_cultures():
    with open("../Input/cultures.json") as culturess:
        culturess = j.load(culturess)
    culture_header = culturess["header"]
    global culture_tags
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
    global race_tags
    race_tags = races_input["header"]
    for i in range(len(race_tags)):
        race_tag = race_tags[i]
        race_entry = races_input[race_tag]
        create_race(race_entry, race_tag)

def create_race(_entry, _tag):
    new_race = race()
    new_race.create(_entry)
    races[_tag] = new_race

def create_plagues():
    with open("../Input/plague.json") as plague_file:
        plague_file = j.load(plague_file)
    global plague_tags
    plague_tags = plague_file["plagues"]
    plague_tags = plague_tags["all"]
    for i in range(len(plague_tags)):
        tag = plague_tags[i]
        create_plague(plague_file[tag], tag)

def create_plague(_entry, _tag):
    global plagues
    new_plague = plague()
    new_plague.create(_entry)
    plagues[_tag] = new_plague

def read_events():
    with open("../Input/events.json") as event_input:
        event_input = j.load(event_input)
    global events
    events = event_input["events"]

def create_all(): #Creates cultures, races and locations
    create_cultures()
    create_locations()
    create_races()
    create_plagues()
    read_events()

def add_to_population(_person):
    total_population.append(_person)

def create_population(_size:int, _race:str, _culture:str, _location:int=0, _birth_location:str="Old World", _age:str="adult"):
    for i in range(_size):
        create_person(_race, _culture, _location, _birth_location, _age)
    location = locations[_location]
    location.update_free_lists()

def create_person(_race:str, _culture:str, _location:int=0, _birth_location:str="Old World", _age:str="adult"):
    new_person = person()
    new_person.uid = len(total_population)
    new_person.set_random_sex()
    new_person.race = races[_race]
    new_person.culture = cultures[_culture]
    new_person.name = new_person.culture.return_random_name(new_person.isFemale)
    new_person.surname = new_person.culture.return_random_surname()
    new_person.current_location = locations[_location]
    new_person.current_location.add_person(new_person)
    new_person.age = new_person.race.random_age(_age)
    new_person.birth_date = year - new_person.age
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
        if re.is_related(_person, person2, 4) == False and person2.doesReproduce and person2.relations["spouse"] == None:
            viable.append(person2)
    if len(viable) != 0:
        spouse = choice(viable)
        check = randint(0, 20)
        if 6 <= check:
            _person.add_spouse(spouse)

def birth(_mother):
    child = person()
    child.uid = len(total_population)
    child.birth(year, _mother)
    child.race = determin_race(child)
    total_population.append(child)
    check = randint(0, 20)
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

#Events
def plague_control_center(_location, _plague:str="old_pox"):
    _location.infect(plagues, _plague)

def immigration(_count:int, _race:str, _culture:str, _location:int=0, _origin:str="Old World"):
    create_population(_count, _race, _culture, _location, _origin)
#Event manager
def doEvent(_events:list):
    for i in range(len(_events)):
        event = _events[i]
        event_type = event["type"]
        if event_type == "plague":
            plague_control_center(locations[event["location"]], event["plague"])
        elif event_type == "immigration":
            immigration(event["size"], event["race"], event["culture"], event["location"], event["origin"])

def update():
    population = 0
    for i in range(len(locations)):
        place = locations[i]
        place.update(year, plagues, plague_tags)
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
                            check = randint(0, 20)
                            if dude.race.isCompatible(dude.relations["spouse"].race) and dude.race.pregnancy_challenge < check and dude.relations["spouse"].isAlive == True:
                                birth(dude)
                elif dude.doesReproduce and dude.relations["spouse"] == None:
                    marriage(dude, dude.current_location)
                if dude.relations["spouse"] == None and dude.age < dude.race.old:
                    doMigrate(dude)
                if dude.race.old < dude.age:
                    check = randint(0, 20) + (dude.race.life_expectancy / dude.age)
                    challenge = 10 + death_modifiers(dude)
                    if challenge < check:
                        death(dude)

            population += len(inhabitans)
    try:
        if events[str(year)]:
            event_entries = events[str(year)]
            doEvent(event_entries)
    except KeyError:
        pass
    if population <= 30:
        race_tag = choice(race_tags)
        race_culture = choice(races[race_tag].cultures)
        create_population(35, race_tag, race_culture)

    if doPrint == True: print("Year: "+str(year)+" | Population: "+str(population))

#Running code
create_all()
if doPrint == True: print("Setup - Finished")
doEvent(events["start"])
for i in range(start_year, end_year+1):
    year = i
    update()
if doPrint == True: print("Export data...")
jex.convertData(total_population, Seed, doPrint)
il.rename_file("output_raw.json", str(Date)+".json")
il.move_file(str(Date)+".json", "../Output/"+str(Date)+".json")
print("...Finished")
if auto_viewer:
    print("Opening JsonViewer")
    exec(open("json_viewer.py").read())
