def isSibling(_person1, _person2):
    #Returns True if both are Siblings
    if _person1.parents == None or _person2.parents == None:
        return False
    if any(i in _person1.parents for i in _person2.parents):
        return True
    else:
        return False

def isCloseRelative(_person1, _person2):
    #Returns True if both are uncle/aunt-niece/nephew pair
    if _person1.parents == None or _person2.parents == None:
        return False
    if any(i in _person1.parents for i in [_person2]) or any(i in _person2.parents for i in [_person1]):
        return True
    else:
        return False

def isCousin(_person1, _person2):
    #Returns True if both are 1st Degree Cousins
    if _person1.parents == None or _person2.parents == None:
        return False
    if any(i in _person1.grandparents for i in _person2.grandparents):
        return True
    else:
        return False

def is2ndCousin(_person1, _person2):
    #Returns True if both are 2nd Degree Cousins
    if _person1.parents == None or _person2.parents == None:
        return False
    if any(i in _person1.greatGrandparents for i in _person2.greatGrandparents):
        return True
    else:
        return False

def isRelated(_person1, _person2, _degree:int=1): #_degree tells the function how far out to search
    #Returns True if both are related
    if _person1.parents == None or _person2.parents == None:
        return False

    if _degree == 0:
        return False
    elif isSibling(_person1, _person2) == True and 1 <= _degree:
        return True
    elif isCloseRelative(_person1, _person2) == True and 1 <= _degree:
        return True
    elif isCousin(_person1, _person2) == True and 2 <= _degree:
        return True
    elif is2ndCousin(_person1, _person2) == True and 3 <= _degree:
        return True
    else:
        return False

def calcR(A, B):

    pass

def getAncestors(start, depth:int=3):
    ancestors = dict()
    ancestors["0"] = [start]
    ancestorList = list()
    ancestorList.append(start)
    rootAncestors = dict() #Ancestors that don't have any recorded parents
    halfRootAncestors = dict() #Ancestors that only have one recorded parent
    for i in range(depth):
        current = ancestors[str(i)]
        next = list() #Stores all ancestors of the current generation
        for ii in range(len(current)):
            ancestor = current[ii]
            ancestorList.append(ancestor)
            if ancestor.parents == None:
                try:
                    rootAncestors[str(i)].append(ancestor)
                except KeyError:
                    rootAncestors[str(i)] = list([ancestor])
                continue
            elif len(ancestor.parents) < 2:
                try:
                    halfRootAncestors[str(i)].append(ancestor)
                except KeyError:
                    halfRootAncestors[str(i)] = list([ancestor])
            next.extend(ancestor.parents) #Adds the parents of the current ancestor to the list
        try:
            halfRootAncestors[str(i)] = len(set(halfRootAncestors[str(i)]))
        except KeyError:
            pass
        try:
            rootAncestors[str(i)] = len(set(rootAncestors[str(i)]))
        except KeyError:
            pass
        try:
            ancestors[str(i)] = len(set(ancestors[str(i)]))
        except KeyError:
            pass
        ancestors[str(i+1)] = next #Creates new entry in the dict for the generation we fetched
    return [ancestors, ancestorList, rootAncestors, halfRootAncestors]

def calcInbreeding(start, depth:int=3):
    input = getAncestors(start, depth)
    ancestorList = input[1]
    maximumUniqueAncestorCount = 2**(depth+1) - 1 #How many ancestors
    trueUniqueAncestorCount = 0

    for generationKey in input[0].keys():
        Ancestors = input[0][generationKey]
        if type(Ancestors) == type(list()):
            input[0][generationKey] = 0

    keys = list(input[0].keys())
    end = False
    for generationKey in keys:
        Ancestors = input[0][generationKey]

        nextKey = str(int(generationKey)+1)

        try:
            halfRootAncestors = input[3][generationKey]
        except KeyError:
            halfRootAncestors = 0

        try:
            RootAncestors = input[2][generationKey]
        except KeyError:
            RootAncestors = 0

        if 0 < RootAncestors and end == False:
            unknownAncestors = 2*RootAncestors
            input[0][nextKey] += unknownAncestors
            try:
                input[2][nextKey] += unknownAncestors
            except KeyError:
                input[2][nextKey] = unknownAncestors

        if 0 < halfRootAncestors and end == False:
            unknownAncestors = 1*halfRootAncestors
            input[0][nextKey] += unknownAncestors
            try:
                input[2][nextKey] += unknownAncestors
            except KeyError:
                input[2][nextKey] = unknownAncestors

        if int(nextKey) == int(keys[-1]):
            end = True

    for generationKey in keys:
        Ancestors = input[0][generationKey]
        trueUniqueAncestorCount += Ancestors

    AVK = round(1 - trueUniqueAncestorCount / maximumUniqueAncestorCount, 4)
    return(AVK)
