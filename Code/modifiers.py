from relation import is_sibling, is_cousin, is_close_relative, is_2nd_cousin,is_related


def death_modifiers(_person):
    modifier = 0
    if 0 <= _person.age < _person.race.adult:
        modifier -=1
    elif _person.race.adult <= _person.age < _person.race.old:
        modifier +=0
    elif _person.race.old <= _person.age < _person.race.ancient:
        modifier +=1
    elif _person.race.ancient <= _person.age:
        modifier += 2**round(_person.race.ancient/_person.age)
    else:
        modifier +=0

    k = _person.current_location.size
    p = len(_person.current_location.inhabitans)

    if k < p:
        modifier += 2**int(p/(k))

    return modifier

def child_mortality_modifiers(_child):
    modifier = 0
    k = _child.current_location.size
    p = len(_child.current_location.inhabitans)
    if k < p:
        modifier += 2**(p/k)

    if is_related(_child.relations["father"], _child.relations["mother"]):
        modifier += 4
    elif is_cousin(_child.relations["father"], _child.relations["mother"]):
        modifier += 3
    elif is_2nd_cousin(_child.relations["father"], _child.relations["mother"]):
        modifier += 2
    else:
        modifier -=1

    return modifier

def marriage_modifiers(_searcher, _spouse):
    modifier = 0
    searcher_rank = _searcher.rank

    if _spouse.race.adult <= _spouse.age <= _spouse.race.old:
        modifier += 1
    if _spouse.rank == searcher_rank:
        modifier += 2
    elif searcher_rank - 1 < _spouse.rank < searcher_rank:
        modifier += 1
    elif searcher_rank < _spouse.rank < searcher_rank + 1:
        modifier += 1
    else:
        modifier -= 1

    if  _searcher.race.life_expectancy * 1.5 < _spouse.race.life_expectancy or _spouse.race.life_expectancy * 1.5 < _searcher.race.life_expectancy:
        modifier -= 2

    return modifier
