import numpy as np
import random
import NetworkX as nx

map_size = 10 #How many nodes the map has

class Map():
    def __init__(self):
        self.nodes = []

class node():
    def __init__(self):
        self.pos_y = ""
        self.pos_x = ""
        self.connections = [] #Should be between 1 and 4
