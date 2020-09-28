# Add imports here
#Mesa Imports
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
#Other Imports
import time
import random
import csv
import numpy as np

# Simulation Status
running = True
go_normal = False
go_fast = False
go_very_fast = False
events = True
# Time
tts = 1  # Total Timesteps
month = 1
year = 1
end_year = 100
# Amount of Pops & related stuff; 1 Pop = 1k People
P = 1
cGrowth = 0
pg = 1
dm = 0
gm = 0
bGrowth = 100
default_growth = 100
n_growth = 0
K = 50  # Supplies for Pops
plague_timer = 0
plague = False
great_plague = False

# Set-Up
cGrowth = cGrowth + (bGrowth * (pg + gm - dm))
bGrowth = default_growth * (pg + gm - dm)

class pop(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.job = job
    def get_job(self):
        pass
    def step(self):
        print("Pop: "+str(self.unique_id))

class PopModel(Model):
    def __init__(self):
        self.schedule = RandomActivation(self)
    def step(self):
        self.schedule.step()

def write_file(month, year, tts, P):
    # Write into save_file.txt
    file.write(str(month) + ";" + str(year) + ";" + str(tts) + ";" + str(P) + '\n')


def print_data(month, year, P, bGrowth):
    print(
        "Month: " + str(month) + " Year: " + str(year) + "\n" + "Population: " + str(P) + "K" + "\n" + "Growth: " + str(
            bGrowth))


def output_data(month, year, tts, P, bGrowth):
    # Write into save_file.txt
    file.write(str(month) + ";" + str(year) + ";" + str(tts) + ";" + str(P) + '\n')
    print(
        "Month: " + str(month) + " Year: " + str(year) + "\n" + "Population: " + str(P) + "K" + "\n" + "Growth: " + str(
            bGrowth))


localtime = time.asctime(time.localtime(time.time()))
file = open("save_file.csv", "w", newline='')
file.write("Simulation started on the " + str(localtime) + "\n" + "Month;Year;Total Timesteps;Pops" + '\n')
output_data(month, year, tts, P, bGrowth)
# Running Code
while running is True:
    if P <= 0:
        running = False
        print("ERROR")
    tts = tts + 1
    dm = (P / K)  # Reduce Pop Growth with larger populations
    if plague is True:  # Plague Updater
        plague_timer -= 1
        dm = dm + 0.75
        if plague_timer == 0:
            plague = False
    elif great_plague is True:
        plague_timer -= 1
        P = P - 1
        if plague_timer == 0:
            great_plague = False
    # Census
    bGrowth = default_growth * (pg + (gm - dm))
    round(bGrowth)
    if cGrowth >= 1000:
        n_growth = round(cGrowth / 1000)
        cGrowth = cGrowth - (n_growth * 1000)
        P = P + n_growth
    elif cGrowth <= -1000:
        n_growth = round(cGrowth / 1000)
        cGrowth = cGrowth - (n_growth * 1000)
        P = P - n_growth
    else:
        cGrowth = cGrowth + bGrowth
    if events is True:  # Events and similar things
        EventList = ["None"] * 20 + ["P-Boom"] * 5 + ["Plague"] * 2
        # + ["Great Plague"]*1
        event = random.choice(EventList)
        if event == "None":
            dm = 0
            gm = 0
            dm = (P / K)  # Reduce Pop Growth with larger populations
        elif event == "Plague" and great_plague is False:
            plague_timer = 6
            plague = True
            dm = dm + 0.5
        elif event == "Great Plague" and great_plague is False:
            plague_timer = 5
            great_plague = True
        elif event == "P Boom" and plague is False:
            gm = gm + 1
    else:
        pass

    # Time Keeper Code
    if month == 12:
        month = 1
        year = year + 1
        if year != end_year:
            print_data(month, year, P, bGrowth)
            write_file(month, year, tts, P)
            print("")  # To make printed output easy to read
    else:
        month = month + 1
    # Printer
    if year == end_year:
        output_data(month, year, tts, P, bGrowth)
        print("Simulation has Ended")
        localtime = time.asctime(time.localtime(time.time()))
        file.write("Simulation has Ended" + '\n' + "Simulation ended on the " + str(localtime))
        # file.write("Simulation ended on the "+str(localtime))
        file.close()
        running = False
    else:
        if go_normal is True:
            time.sleep(1)
        elif go_fast is True:
            time.sleep(0.5)
        elif go_very_fast is True:
            time.sleep(0.25)
        else:
            pass
