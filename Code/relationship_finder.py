def is_sibling(p1, p2):
    """
    Checks if p1 and p2 are siblins or not, returns boolean
    """
    if p1.father[0] == p2.father[0] or p1.mother[0] == p2.mother[0]:
        return True
    else:
        return False

def is_cousin(p1, p2):
    """
    Checks if p1 and p2 are cousins or not, returns boolean
    """
    if any(i in p1.grandparents for i in p2.grandparents): #Checks if any person in p1.grandparents is in p2.grandparents
        return True
    else:
        return False

def is_2nd_cousin(p1, p2):
    """
    Checks if p1 and p2 are second cousins, returns boolean
    """
    if any(i in p1.great_grandparents for i in p2.great_grandparents):
        return True
    else:
        return False

def is_close_relative(p1, p2):
    """
    Checks if p1 and p2 are in an aunt/uncle-niece/nephew relation, returns boolean
    """
    if is_sibling(p1.father[0], p2) == True or is_sibling(p1.mother[0], p2) == True:
        return True
    elif is_sibling(p2.father[0], p1) == True or is_sibling(p2.mother[0], p1) == True:
        return True
    else:
        return False
