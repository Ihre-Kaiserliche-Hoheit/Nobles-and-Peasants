def is_sibling(_person1, _person2):
    #Returns True if both are Siblings
    if any(i in _person1.relations["parents"] for i in _person2.relations["parents"]):
        return True
    else:
        return False

def is_close_relative(_person1, _person2):
    #Returns True if both are uncle/aunt-niece/nephew pair
    if any(i in _person1.relations["parents"] for i in [_person2]) or any(i in _person2.relations["parents"] for i in [_person1]):
        return True
    else:
        return False

def is_cousin(_person1, _person2):
    #Returns True if both are 1st Degree Cousins
    if any(i in _person1.relations["grandparents"] for i in _person2.relations["grandparents"]):
        return True
    else:
        return False

def is_2nd_cousin(_person1, _person2):
    #Returns True if both are 2nd Degree Cousins
    if any(i in _person1.relations["great grandparents"] for i in _person2.relations["great grandparents"]):
        return True
    else:
        return False

def is_related(_person1, _person2, _degree:int=1): #_degree tells the function how far out to search
    #Returns True if both are related
    if _person1.relations["parents"] == None or _person2.relations["parents"] == None:
        return False

    if _degree == 0:
        return False
    elif is_sibling(_person1, _person2) == True and 0 < _degree:
        return True
    elif is_close_relative(_person1, _person2) == True and 0 < _degree:
        return True
    elif is_cousin(_person1, _person2) == True and 1 < _degree:
        return True
    elif is_2nd_cousin(_person1, _person2) == True and 2 < _degree:
        return True
    else:
        return False
