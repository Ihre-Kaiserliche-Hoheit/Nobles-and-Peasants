from random import randint

def roll(_number:int=1, _size:int=20, _mods:int=0):
    result = _mods
    for i in range(_number):
        result += randint(0,_size)
    return(result)
