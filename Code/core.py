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
cultures = {}
culture_tags = []
races = {}
race_tags = []
year = start_year
population = settings["start_population"]
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

def read_events():
    with open("../Input/events.json") as event_input:
        event_input = j.load(event_input)
    global events
    events = event_input["events"]

def create_all(): #Creates cultures, races and locations
    create_cultures()
    create_locations()
    create_races()
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
        spouse = r.choice(viable)
        check = r.randint(0, 20)
        if 6 <= check:
            _person.add_spouse(spouse)

def birth(_mother):
    child = person()
    child.uid = len(total_population)
    child.birth(year, _mother)
    child.race = determin_race(child)
    total_population.append(child)
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

#Events
def plague(_start_location, _plague:str="Pox"):
    _start_location.infect()

def immigration(_count:int, _race:str, _culture:str, _location:int=0):
    create_population(_count, _race, _culture)
#Event manager
def doEvent(_events:list):
    for i in range(len(_events)):
        event = _events[i]
        event_type = event["type"]
        if event_type == "plague":
            plague(locations[event["location"]], event["plague"])
        elif event_type == "immigration":

            immigration(event["size"], event["race"], event["culture"], locations[event["location"]])

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
                            if dude.race.isCompatible(dude.relations["spouse"].race) and dude.race.pregnancy_challenge < check and dude.relations["spouse"].isAlive == True:
                                birth(dude)
                elif dude.doesReproduce and dude.relations["spouse"] == None:
                    marriage(dude, dude.current_location)
                if dude.relations["spouse"] == None and dude.age < dude.race.old:
                    doMigrate(dude)
                if dude.race.old < dude.age:
                    check = roll(_mods=(dude.race.life_expectancy / dude.age))
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
    if population <= 50:
        race_tag = r.choice(race_tags)
        race_culture = r.choice(races[race_tag].cultures)
        create_population(20, race_tag, race_culture)
        locations[0].infect()

    if doPrint == True: print("Year: "+str(year)+" | Population: "+str(population))

def PersonToDict(_person):
    entry = dict()
    entry["ID"] = _person["uid"]
    entry["Name"] = _person["name"]
    entry["Patronym"] = _person["patronym"]
    entry["Surname"] = _person["surname"]
    if _person["isFemale"] == True:
        entry["Sex"] = "F"
    else:
        entry["Sex"] = "M"
    entry["Culture"] = _person["culture"].name
    entry["Race"] = _person["race"].name
    relations = _person["relations"]
    if relations["father"] != None:
        father = vars(relations["father"]) #For some fucking reason I need to do this black magic instead of a simple entry["Father"] = _person.relations["father"].uid
        entry["Father"] = father["uid"]
    else:
        entry["Father"] = None

    if relations["mother"] != None:
        mother = vars(relations["mother"]) #For some fucking reason I need to do this black magic instead of a simple entry["Mother"] = _person.relations["mother"].uid
        entry["Mother"] = mother["uid"]
    else:
        entry["Mother"] = None

    if relations["spouse"] != None:
        spouse = vars(relations["spouse"]) #For some fucking reason I need to do this black magic instead of a simple entry["Mother"] = _person.relations["mother"].uid
        entry["Spouse"] = spouse["uid"]
    else:
        entry["Spouse"] = None

    children = relations["children"]
    if children != None:
        ch = list()
        for i in range(len(children)):
            child = children[i]
            ch.append(child.uid)

        entry["Children"] = ch
    else:
        entry["Children"] = None
    del children
    del relations
    entry["Birth Date"] = str(_person["birth_date"])
    entry["Birth Place"] = _person["birth_location"]
    entry["Alive"] = _person["isAlive"]
    entry["Age"] = _person["age"]
    if _person["isAlive"] == False:
        entry["Death Date"] = str(_person["death_date"])
        entry["Death Place"] = _person["death_location"]

    return entry

def convert_data():
    data = {}
    entries = {}
    data["Header"] = {
    "Length":len(total_population),
    "Seed":Seed
    }
    for i in range(len(total_population)):
        if doPrint == True and i%300 == 0:
            print(str(round((i/len(total_population)*100), 2)) + "% done")
        per = vars(total_population[i])
        entry = PersonToDict(per)
        ID = str(entry["ID"])
        entries[ID] = entry

    if doPrint == True: print("100% done")
    data["Entries"] = entries
    output = open("output_raw.json", "w")
    if doPrint == True: print("Saving data...")
    import jsbeautifier
    opt = jsbeautifier.default_options()
    opt.indent_size = 2
    data = jsbeautifier.beautify(j.dumps(data, ensure_ascii=False), opt)
    output.write(data)
    output.close()
    if doPrint == True: print("...Saved data")

#Running code
create_all()
if doPrint == True: print("Setup: Part I - Finished")
create_population(settings["start_population"], "Elf", races["Elf"].cultures[0], _birth_location="New World")
if doPrint == True: print("Setup: Part II - Finished")

for i in range(start_year, end_year+1):
    year = i
    update()
if doPrint == True: print("Export data...")
convert_data()
il.rename_file("output_raw.json", str(Date)+".json")
il.move_file(str(Date)+".json", "../Output/"+str(Date)+".json")
print("...Finished")
if auto_viewer:
    exec(open("json_viewer.py").read())
