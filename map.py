import numpy as np
import random
import csv
import webbrowser
Map3 = ""
Map2 = ""
Map = []
y_in = 50 #Height of the Map
x_in = 100 #Width of the Map
biom_list = ["Water", "Land"]

class Map_row():
    def __init__(self):
        self.Tiles = []

class Tile():
    def __init__(self):
        self.pos_y = ""
        self.pos_x = ""
        self.biom = ""
        self.symbole = ""

#Generate Map
for y in range(y_in):
    Row = Map_row()
    for x in range(x_in):
        New_Tile = Tile()
        New_Tile.pos_y = y
        New_Tile.pos_x = x
        New_Tile.biom = random.choice(biom_list)
        if New_Tile.biom == "Land":
            New_Tile.symbole = "L"
        elif New_Tile.biom == "Water":
            New_Tile.symbole = "W"
        Row.Tiles.append(New_Tile)
    Map.append(Row)

#Print Map
for i in range(len(Map)):
    Read = Map[i]
    Map2 = Map2+"|"
    for j in range(len(Read.Tiles)):
        Tile = Read.Tiles[j]
        Map2 = Map2+str(Tile.symbole)
        #Map2 = Map2+"("+str(Tile.pos_y)+"|"+str(Tile.pos_x)+")"
    Map2 = Map2+"|"+"\n"
print(Map2)
print("-------------------")
for i in range(len(Map)):
    Read = Map[i]
    for j in range(len(Read.Tiles)):
        Tile = Read.Tiles[j]
        #Map3 = Map3+str(Tile.symbole)
        Map3 = Map3+"("+str(Tile.pos_y)+"|"+str(Tile.pos_x)+")"
    Map3 = Map3+"|"+"\n"
print(Map3)
