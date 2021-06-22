"""
Just general file managment code that I may or may not repurpos in every project
that needs to interact with files, so most of my programs
OC - DO NOT STEAL MY UNIQUE SONIC OC UWU
"""


import os
import shutil as sht
from datetime import datetime as d
import random as r
import hashlib as has


class EmptyListError(Exception):
    """
    Error for cases where a list with content is expected but non is found
    """
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
    """
    Gives the time in the following format:
        YEAR.MONTH.DAY HOUR:MINUTE:SECOND
    """
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
        new_list = r.choices(List, k=amount)
        return(new_list)

def convert_to_hash(_input, _length=None):
    _input = str(_input)
    if _length != None:
        output = int(has.sha256(_input.encode('utf-8')).hexdigest(), 16) % 10**_length
    else:
        output = int(has.sha256(_input.encode('utf-8')).hexdigest(), 16)
    return(output)

def pseudo_random_seed():
    seed = get_time()
    seed = convert_to_hash(seed)
    return(seed)
