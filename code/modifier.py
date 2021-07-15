from relation import isRelated, isSibling, calcInbreeding

def modifierDeath(inputPerson):
    modifier = 0

    if inputPerson.race.seniorAge <= inputPerson.age:
        modifier += (inputPerson.age / inputPerson.race.seniorAge) - 1

    if inputPerson.currentPlace.populationCapacity < len(inputPerson.currentPlace.population):
        modifier += 0.1**(len(inputPerson.currentPlace.population) / inputPerson.currentPlace.populationCapacity)

    modifier += inputPerson.inbreeding

    if inputPerson.plague != None:
        modifier += inputPerson.plague.deadliness

    return modifier

def modifierMarriage(inputSearcher, inputTarget):
    modifier = 0

    if isSibling(inputSearcher, inputTarget):
        modifier -= 0.8
    if isRelated(inputSearcher, inputTarget, 4):
        modifier -= 0.3

    if inputSearcher.rank == inputTarget.rank:
        modifier += 0.2
    elif inputSearcher.rank <  inputTarget.rank:
        modifier += 0.1
    elif inputTarget.rank < inputSearcher.rank:
        modifier -= 0.1

    if 1 < len(inputTarget.oldSpouses):
        modifier += 0.05

    return modifier
