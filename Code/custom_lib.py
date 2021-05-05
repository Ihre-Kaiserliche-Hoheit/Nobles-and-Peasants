import os
import shutil as sht
from datetime import datetime as d
import random as r


#Just general file managment code that I may or may not repurpos in every project
#that needs to interact with files, so most of my programs
#OC - DO NOT STEAL MY UNIQUE SONIC OC UWU


class EmptyListError(Exception):
    pass


def txt_to_list(filename):
    file = open(filename, "r")
    file = file.read().splitlines()
    return(file)

def delete_file(filename):
    os.remove(filename)

def delete_folder(foldername):
    sht.rmtree(foldername)

def rename_file(filename, new_name):
    os.rename(filename, new_name)


def move_file(file, target):
    sht.move(file, target)

def get_time():
    #Gives the time in the following format:
    # YEAR.MONTH.DAY HOUR:MINUT:SECOND
    time = d.now()
    t = str(time.strftime("%Y.%m.%d %H:%M:%S"))
    return(t)

def create_random_list_from(List:list, amount:int):
    if len(List) == 0:
        #Raise error of the list is empty
        raise EmptyListError
    elif len(List) <= amount:
        #Just returns the list because it would do it anyway, I just cut corners here
        return(List)
    else:
        new_list = []
        while len(new_list) < amount+1:
            item = r.choices(List)
            item = item[0] #The reason for this is black magic
            if item not in new_list:
                new_list.append(item)
        return(new_list)
