import json as j


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

def convertData(_total_population:list, _seed, _doPrint:bool):
    data = {}
    entries = {}
    data["Header"] = {
    "Length":len(_total_population),
    "Seed":_seed
    }
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
    if _doPrint == True: print("...Saved data")
