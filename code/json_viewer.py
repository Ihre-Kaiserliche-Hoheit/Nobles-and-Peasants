#Version 1.3
from tkinter import *
from tkinter.ttk import Combobox
import json
from os import listdir
import igraph as ig

top = Tk()
top.resizable(False, False)
top.geometry("400x430")
top.wm_title("Viewer")

file = "../output/"
entries = None

#colours
default_colour = "white smoke"
female_colour = "IndianRed1"
male_colour = "RoyalBlue1"
no_colour = "red"
yes_colour = "green2"


child_buttons = []
spouse_options = []
#Searchbar
def searchbar_pressed():
    input = searchbar_entry.get()
    getEntry(input)


    print(input)

def update_searchbar():
    searchbar_entry["bg"] = default_colour
    top.after(5000, update_searchbar)

#Json selection and import
def select_file():
    outer_top = Toplevel()
    outer_top.resizable(False, True)
    outer_top.geometry("400x200")
    outer_top.wm_title("Choose File")
    files = listdir("../output")
    files.sort()
    site_box = Frame(outer_top)
    site_box.pack(side=RIGHT)
    global file_list
    file_list_scollbar = Scrollbar(outer_top)
    file_list_scollbar.pack(side = RIGHT, fill = Y)
    file_list = Listbox(outer_top, height=(len(files)), selectmode=SINGLE, width=30, yscrollcommand=file_list_scollbar.set)
    for i in range(len(files)):
        file_list.insert(0, files[i])
    file_list.pack(side=LEFT, fill = BOTH)
    file_list_scollbar.config(command=file_list.yview)
    selection_label = Label(site_box, text="Select a .json in /output")
    selection_label.pack(side=TOP)
    confirm_file = Button(site_box, text="Confirm", command=import_file)
    confirm_file.pack()

def import_file():
    try:
        filename_input = str(file_list.get(ANCHOR))
        global entries
        with open(file+filename_input) as json_file:
            entries = json.load(json_file)
        entries = entries["Entries"]
        file_list["bg"]=yes_colour
        getEntry("0") #Out jumps to the first entry after importing
    except IsADirectoryError:
        file_list["bg"]=no_colour
    except json.JSONDecodeError:
        file_list["bg"]=no_colour

def getEntry(_id:str):
    try:
        entry = entries[str(_id)]
        ID_label2["text"] = entry["ID"]
        WholeName_label2["text"] = entry["Name"] + " " + entry["Surname"]
        Sex_label2["text"] = entry["Sex"]
        Rank_label2["text"] = entry["Rank"]
        Race_label2["text"] = entry["Race"]
        Culture_label2["text"] = entry["Culture"]
        if entry["Father"] != None:
            Father_label2["text"] = entry["Father"]
        else:
            Father_label2["text"] = ""
        if entry["Father"] != None:
            Mother_label2["text"] = entry["Mother"]
        else:
            Mother_label2["text"] = ""
        spouseList = list()
        #if entry["Old Spouse"] != None:
        #    spouseList.extend(entry["Old Spouse"])

        if len(spouseList) == 0:
            Spouse_list["values"] = "None"
        else:
            Spouse_list["values"] = spouseList
            Spouse_list.set(spouseList[0])

        if len(spouseList) != 0:
            if entry["Sex"] == "Male":
                Spouse_label2["bg"] = female_colour
            else:
                Spouse_label2["bg"] = male_colour
        else:
            Spouse_label2["bg"] = default_colour


        updateChildren()
        BirthDate_label2["text"] = entry["Birth Date"]
        BirthPlace_label2["text"] = entry["Birth Place"]
        try:
            DeathDate_label2["text"] = entry["Death Date"]
        except KeyError:
            DeathDate_label2["text"] = ""
        try:
            DeathPlace_label2["text"] = entry["Death Place"]
        except KeyError:
            DeathPlace_label2["text"] = ""
        Age_label2["text"] = entry["Age"]
        searchbar_entry["bg"] = yes_colour
    except KeyError:
        searchbar_entry["bg"] = no_colour
    except TypeError:
        searchbar_entry["bg"] = no_colour

def updateChildren(event=None):
    entry = entries[str(ID_label2["text"])]
    children_entry = entry["Children"]
    global child_buttons
    for i in range(len(child_buttons)):
        #Cleans the children buttons to prevent the wrong buttons from appearing
        button = child_buttons[i]
        button.destroy()
    child_buttons = list()
    if children_entry != None:
        for i in range(len(children_entry)):
            child = children_entry[i]
            child2 = entries[str(child)]
            spouse_id = int(Spouse_list.get())
            if ((child2["Father"] == entry["ID"] and child2["Mother"] == spouse_id) or
                (child2["Father"] == spouse_id and child2["Mother"] == entry["ID"])):
                if child2["Sex"] == "Male":
                    colour = male_colour
                else:
                    colour = female_colour
                child_button = Button(Children_subframe, text=child, command=lambda text=str(child):getEntry(text), bg=colour)
                child_button.grid(row=0, column=i)
                child_buttons.append(child_button)

def getAllDescendants(_root, _depth:int=4):
    """
    Gets a list of a descendants _depth generations deep
    """
    generations = {
    "0":{
        str(_root["ID"]):_root["Children"]
        }
    }
    members = list()
    for i in range(_depth):
        generation = generations[str(i)]
        next_generation = dict()
        for person in generation:
            person_entry = entries[str(person)]
            members.append(person_entry["ID"])
            children = person_entry["Children"]
            if children != None:
                for child in children:
                    entry = entries[str(child)]
                    next_generation[str(entry["ID"])] = entry["Children"]

        generations[str(i+1)] = next_generation
    members = list(set(members))
    members.sort()
    return [generations, members]

def graph_descendant_all():
    graph_boy = ig.Graph()

    root = entries[str(ID_label2["text"])]
    out = getAllDescendants(root)

    g_layout = graph_boy.layout("tree", 0)
    #ig.plot(graph_boy, layout=g_layout)


#Menu
menubar = Menu(top)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import File", command=select_file)
menubar.add_cascade(label="File", menu=filemenu)
graphmenu = Menu(menubar, tearoff=0)
graphmenu.add_command(label="Graph - Descendants(All)", command=graph_descendant_all)
menubar.add_cascade(label="Graphs - Not Working", menu=graphmenu)


#Searchbar
searchbar_frame = Frame(top)
searchbar_frame.pack(side=TOP)
searchbar_subframe2 = Frame(searchbar_frame)
searchbar_subframe2.pack()
searchbar_subframe1 = Frame(searchbar_frame)
searchbar_subframe1.pack()
searchbar_entry = Entry(searchbar_subframe1)
searchbar_entry.pack(side=LEFT)
searchbar_button = Button(searchbar_subframe1, text="Search", bg=default_colour, command=searchbar_pressed)
searchbar_button.pack(side=RIGHT)
searchbar_label = Label(searchbar_subframe2, text="Input Character ID")
searchbar_label.pack(side=BOTTOM)


#Person Entry
ID_frame = Frame(top)
ID_frame.pack()
ID_label = Label(ID_frame, text="ID")
ID_label.pack(side=LEFT)
ID_label2 = Button(ID_frame, state=DISABLED)
ID_label2.pack(side=LEFT)

WholeName_frame = Frame(top)
WholeName_frame.pack()
WholeName_label = Label(WholeName_frame, text="Name:")
WholeName_label.pack(side=LEFT)
WholeName_label2 = Label(WholeName_frame)
WholeName_label2.pack(side=LEFT)

Sex_frame = Frame(top)
Sex_frame.pack()
Sex_label = Label(Sex_frame, text="Sex:")
Sex_label.pack(side=LEFT)
Sex_label2 = Label(Sex_frame)
Sex_label2.pack(side=LEFT)

Rank_frame = Frame(top)
Rank_frame.pack()
Rank_label = Label(Rank_frame, text="Rank:")
Rank_label.pack(side=LEFT)
Rank_label2 = Label(Rank_frame)
Rank_label2.pack(side=LEFT)

Race_frame = Frame(top)
Race_frame.pack()
Race_label = Label(Race_frame, text="Race:")
Race_label.pack(side=LEFT)
Race_label2 = Label(Race_frame)
Race_label2.pack(side=LEFT)

Culture_frame = Frame(top)
Culture_frame.pack()
Culture_label = Label(Culture_frame, text="Culture:")
Culture_label.pack(side=LEFT)
Culture_label2 = Label(Culture_frame)
Culture_label2.pack(side=LEFT)

Father_frame = Frame(top)
Father_frame.pack()
Father_label = Label(Father_frame, text="Father:")
Father_label.pack(side=LEFT)
Father_label2 = Button(Father_frame, command=lambda:getEntry(Father_label2["text"]), bg=male_colour)
Father_label2.pack(side=LEFT)

Mother_frame = Frame(top)
Mother_frame.pack()
Mother_label = Label(Mother_frame, text="Mother:")
Mother_label.pack(side=LEFT)
Mother_label2 = Button(Mother_frame, command=lambda:getEntry(Mother_label2["text"]), bg=female_colour)
Mother_label2.pack(side=LEFT)

Spouse_frame = Frame(top)
Spouse_frame.pack()
Spouse_label = Label(Spouse_frame, text="Spouse:")
Spouse_label.pack(side=LEFT)
Spouse_selection = Frame(Spouse_frame)
Spouse_label2 = Button(Spouse_selection, text="Go", command=lambda:getEntry(Spouse_list.get()), bg=default_colour)
Spouse_label2.pack(side=LEFT)
Spouse_list = Combobox(Spouse_selection, textvariable="Spouses", values=spouse_options, width=8)
Spouse_list.pack(side=LEFT)
Spouse_selection.pack(side=LEFT)
Spouse_list.bind("<<ComboboxSelected>>", updateChildren)

Children_frame = Frame(top)
Children_frame.pack()
Children_label = Label(Children_frame, text="Children:")
Children_label.pack(side=LEFT)
Children_subframe = Frame(Children_frame)
Children_subframe.pack(side=LEFT)

Children_label2 = Label(Children_frame)
Children_label2.pack(side=LEFT)

BirthDate_frame = Frame(top)
BirthDate_frame.pack()
BirthDate_label = Label(BirthDate_frame, text="Birth Date:")
BirthDate_label.pack(side=LEFT)
BirthDate_label2 = Label(BirthDate_frame)
BirthDate_label2.pack(side=LEFT)

BirthPlace_frame = Frame(top)
BirthPlace_frame.pack()
BirthPlace_label = Label(BirthPlace_frame, text="Birth Place:")
BirthPlace_label.pack(side=LEFT)
BirthPlace_label2 = Label(BirthPlace_frame)
BirthPlace_label2.pack(side=LEFT)

DeathDate_frame = Frame(top)
DeathDate_frame.pack()
DeathDate_label = Label(DeathDate_frame, text="Death Date:")
DeathDate_label.pack(side=LEFT)
DeathDate_label2 = Label(DeathDate_frame)
DeathDate_label2.pack(side=LEFT)

DeathPlace_frame = Frame(top)
DeathPlace_frame.pack()
DeathPlace_label = Label(DeathPlace_frame, text="Death Place:")
DeathPlace_label.pack(side=LEFT)
DeathPlace_label2 = Label(DeathPlace_frame)
DeathPlace_label2.pack(side=LEFT)

Age_frame = Frame(top)
Age_frame.pack()
Age_label = Label(Age_frame, text="Age:")
Age_label.pack(side=LEFT)
Age_label2 = Label(Age_frame)
Age_label2.pack(side=LEFT)

top.config(menu=menubar)

update_searchbar()
top.mainloop()
