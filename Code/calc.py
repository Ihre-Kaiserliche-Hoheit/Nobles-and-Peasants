"""
functions should start with "calc_"
"""

import personal_math as pm

def calc_death_chance(le:int, a:int, cm:float, p:int, k:int): #le - life expectantcy, a - age, cm - child mortality, p - population count, k - carry capacity, e - euler's number
    e = pm.e()
    #Calculates infant mortality, small spike in the first four or so years
    d1 = cm*e**((-5*a*(p/k)))
    #Calculates liklyhood to die because of a critical code error in the code needed to survive - Kaiser
    #Normal people just call it death by natrual causes - Steve
    #d2 = ((50/(1 + e**(-0.19*((a-le)+8)))) / 100)
    d2 = (50/(1+e**(-0.19*((a-le)+8))))/100
    #More general causes of death like being crushed by a blue whale that fell from the sky - Kaiser
    #That isn't a normal cause of death - Steve
    d3 = (0.0004*a+0.00001)*e**(1-a/le)
    dc = round(d1+d2+d3, 8) #Rounds to closes 7th diget after the point, cuz we love precision

    return(dc) #Gib me dat chance
