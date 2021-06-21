#Imports
from person import person
from culture import culture
from location import location
from race import race
from dice import roll

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
    Seed = il.get_time()
else:
    Seed = settings["seed"]
r.seed(Seed)

##Globals
total_population = []
locations = []
culture_list = {}
races = {}
year = start_year

#Functions
def create_cultures():
    with open("../Input/cultures.json") as cultures:
        cultures = j.load(cultures)
    culture_header = cultures["header"]
    culture_tags = culture_header["culture_list"]
    for i in range(len(culture_tags)):
        culture_tag = culture_tags[i]
        culture_entry = cultures[culture_tag]
        create_culture(culture_entry, culture_tag)

def create_culture(_entry, _tag):
    new_culture = culture()
    new_culture.create(_entry)
    culture_list[_tag] = new_culture

def create_locations():
    with open("../Input/world.json") as world:
        world = j.load(world)
    world = world["settlements"]
    for i in range(len(world)):
        location_entry = world[i]
        create_location(location_entry)

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
