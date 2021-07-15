import json as j
import fileManager as fm


def PersonToDict(_person):
    entry = dict()
    entry["ID"] = _person["uid"]
    entry["Name"] = _person["givenName"]
    entry["Surname"] = _person["surname"]
    if _person["isFemale"] == True:
        entry["Sex"] = "Female"
    else:
        entry["Sex"] = "Male"
    entry["Culture"] = _person["culture"].name
    entry["Race"] = _person["race"].name
    if _person["father"] != None:
        father = vars(_person["father"]) #For some fucking reason I need to do this black magic instead of a simple entry["Father"] = _person.relations["father"].uid
        entry["Father"] = father["uid"]
    else:
        entry["Father"] = None

    if _person["mother"] != None:
        mother = vars(_person["mother"]) #For some fucking reason I need to do this black magic instead of a simple entry["Mother"] = _person.relations["mother"].uid
        entry["Mother"] = mother["uid"]
    else:
        entry["Mother"] = None

    spouseIDs = list()
    if _person["spouse"] != None:
        spouse = vars(_person["spouse"])
        spouseIDs.append(spouse["uid"])
    #if _person["spouse"] != None:
    #    spouse = vars(_person["spouse"]) #For some fucking reason I need to do this black magic instead of a simple entry["Mother"] = _person.relations["mother"].uid
    #    entry["Spouse"] = spouse["uid"]
    #else:
    #    entry["Spouse"] = None

    if _person["oldSpouses"] != None:
        if 0 < len(_person["oldSpouses"]):
            spouses = _person["oldSpouses"]
            for i in range(len(_person["oldSpouses"])):
                spouse = vars(spouses[i])
                spouseIDs.append(spouse["uid"])
    #    else:
    #        entry["Old Spouse"] = None
    #else:
    #    entry["Old Spouse"] = None
    spouses = list()
    spouses.extend(spouseIDs)
    entry["Spouses"] = spouses

    children = _person["children"]
    if children != None:
        ch = list()
        for i in range(len(children)):
            child = children[i]
            ch.append(child.uid)

        entry["Children"] = ch
    else:
        entry["Children"] = None
    del children
    if ranks["top"] < _person["rank"]:
        entry["Rank"] = str(ranks["top"])
    else:
        entry["Rank"] = ranks[str(_person["rank"])]
    entry["Birth Date"] = str(_person["birthDate"])
    entry["Birth Place"] = _person["birthPlace"]
    entry["Alive"] = _person["isAlive"]
    entry["Age"] = _person["age"]
    if _person["isAlive"] == False:
        entry["Death Date"] = str(_person["deathDate"])
        entry["Death Place"] = _person["deathPlace"]

    return entry

def convertData(_total_population:list, _seed, _doPrint:bool):
    data = {}
    entries = {}
    data["Header"] = {
    "Length":len(_total_population),
    "Seed":_seed
    }
    global ranks
    with open("../input/ranks.json") as ranks:
        ranks = j.load(ranks)
    for i in range(len(_total_population)):
        if _doPrint == True and i%400 == 0:
            print(str(round((i/len(_total_population)*100), 2)) + "% done")
        person = vars(_total_population[i])
        entry = PersonToDict(person)
        ID = str(entry["ID"])
        entries[ID] = entry

    if _doPrint == True: print("100% done")
    data["Entries"] = entries
    output = open("output_raw.json", "w")
    if _doPrint == True: print("Saving data...")
    fancyExport = False
    if fancyExport == True:
        """
        Currently isn't used but will late become an option in the settings
        """
        import jsbeautifier
        opt = jsbeautifier.default_options()
        opt.indent_size = 2
        data = jsbeautifier.beautify(j.dumps(data, ensure_ascii=False), opt)
    else:
        data = j.dumps(data, ensure_ascii=False)
    output.write(data)
    output.close()

    fm.move_file("output_raw.json", "../output/"+str(_seed)+".json")

    if _doPrint == True: print("...Saved data")
