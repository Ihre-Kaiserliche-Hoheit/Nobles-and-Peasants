"""
This file cointains all function relatet to math that can be reused
"""


import math as m
import random as r


def calc_distance(start, end):
    """
    Input an object that has a pos_x and pos_y attribute
    """
    x = end.pos_x - start.pos_x
    y = end.pos_y - start.pos_y

    distance = m.sqrt(x*x + y*y)

    return(distance)
