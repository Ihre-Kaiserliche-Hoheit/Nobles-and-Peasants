def is_sibling(p1, p2):
    #Checks if p1 and p2 are siblins or not
    if p1.father[0] == p2.father[0] or p1.mother[0] == p2.mother[0]:
        return True
    else:
        return False

def is_cousin(p1, p2):
    #Checks if p1 and p2 are cousins or not
    #I doubt this is the best way to do this function but I have no clue how to do it better
    f1 = p1.father[0]
    m1 = p1.mother[0]
    f2 = p2.father[0]
    m2 = p2.mother[0]
    if (is_sibling(f1, f2) == True      or
        is_sibling(m1, m2) == True      or
        is_sibling(f1, m2) == True      or
        is_sibling(m1, f2) == True      ):
        return True
    else:
        return False
