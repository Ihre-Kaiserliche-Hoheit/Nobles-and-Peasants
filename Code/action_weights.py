"""
functions should start with "weight_"
Add new weight calculations into this file
"""


from relationship_finder import is_sibling, is_cousin


def weight_age(person, modus):
    """
    Returns a weight based on the persons age
    Modi:
    'young' - returns a weight shifted to the younger side
    'medium' - retruns a weight centered
    'old' - returns a weight shifted to the older side
    """
    value = 0
    r2p = 2.5066 #Approximation of root(2pi)
    pi = 3.1416 #Pi to the fourth digit after the comma
    e = 2.7183 #Euler's number to the fourth digit after the comma
    sigma = 0.4
    age = person.age

    if modus == "young":
        mean = 0
    elif modus == "medium":
        mean = 25
    elif modus == "old":
        mean = 60
    else:
        mean = 30 #Default value

    value = ((1/(sigma*r2p))*e**(((age-mean)*(age-mean))/2*(sigma*sigma)))*10 #Bell Curve for the win!

    return(int(round(value, 0)))

def weight_relation(p1, p2):
    """
    Returns a weight dependant on how p1 and p2 are related
    """
    #Most people don't want to marry their close relatives...
    value = 0
    try:
        if is_sibling(p1, p2) == True:
            #Yikes, we ain't in Alabama
            value = -50

        elif is_cousin(p1, p2) == True:
            #Habsburg, get the fuck out
            value = -25

        else:
            value = 10 #Should always be identical to the value in the except-block

    except IndexError: #Because the first gen has no parents
        value = 10

    return(value)

def weight_emigration(person, migrants, avaible_males, avaible_females):
    """
    Returns a weight for the migration mechanic
    """
    amn = len(avaible_males)
    awn = len(avaible_females)
    value = 0

    value += weight_age(person, "medium")

    try:
        father = person.father[0]
        if 3 < len(father.children):
            value += 20*(len(father.children)/5)
    except IndexError:
        value += 20

    if 30 < len(migrants):
        value -= 10*(len(migrants)/30)

    return(int(round(value, 0)))
