def is_sibling(p1, p2):
    """
    Checks if p1 and p2 are siblins or not
    """
    if p1.father[0] == p2.father[0] or p1.mother[0] == p2.mother[0]:
        return True
    else:
        return False

def is_cousin(p1, p2):
    """
    Checks if p1 and p2 are cousins or not
    """
    """
    f1 = p1.father[0]
    m1 = p1.mother[0]
    f2 = p2.father[0]
    m2 = p2.mother[0]
    if (is_sibling(f1, f2) == True      or
        is_sibling(m1, m2) == True      or
        is_sibling(f1, m2) == True      or
        is_sibling(m1, f2) == True      ): #Old way, just leaving it in if anyone wants to see it
    """
    if any(i in p1.grandparents for i in p2.grandparents): #Checks if any person in p1.grandparents is in p2.grandparents
        return True
    else:
        return False

def is_2nd_cousin(p1, p2):
    """
    Checks if p1 and p2 are second cousins
    """
    if any(i in p1.great_grandparents for i in p2.great_grandparents):
        return True
    else:
        return False

def is_close_relative(p1, p2):
    if is_sibling(p1.father[0], p2) == True or is_sibling(p1.mother[0], p2) == True:
        return True
    elif is_sibling(p2.father[0], p1) == True or is_sibling(p2.mother[0], p1) == True:
        return True
    else:
        return False
