from relation import is_sibling, is_cousin, is_close_relative, is_2nd_cousin,is_related


def death_modifiers(_person):
    modifiers = 0
    if 0 <= _person.age < _person.race.adult:
        modifiers -=1
    elif _person.race.adult <= _person.age < _person.race.old:
        modifiers +=0
    elif _person.race.old <= _person.age < _person.race.ancient:
        modifiers +=1
    elif _person.race.ancient <= _person.age:
        modifiers += 2**round(_person.race.ancient/_person.age)
    else:
        modifiers +=0

    return modifiers

def child_mortality_modifiers(_child):
    modifiers = 0
    k = _child.current_location.size
    p = len(_child.current_location.inhabitans)
    if k < p:
        modifiers += 2**(k/p)

    if is_related(_child.relations["father"], _child.relations["mother"]):
        modifiers += 4
    elif is_cousin(_child.relations["father"], _child.relations["mother"]):
        modifiers += 3
    elif is_2nd_cousin(_child.relations["father"], _child.relations["mother"]):
        modifiers += 2
    else:
        modifiers -=1

    return modifiers
