import random

orcsoundL = []
orcsounds = open("OrcSounds.txt", "r", newline="")
orcsoundL = orcsounds.read().splitlines()
orcsounds.close()
orcnameM = open("OrcMaleNames.txt", "w", newline="")
orcnameF =open("OrcFemaleNames.txt", "w", newline="")
orcnameL =open("OrcLastNames.txt", "w", newline="")
orcM = []
orcF = []
orcL = []


for j in range(200):
    for i in range(len(orcsoundL)):
        sound1 = random.choice(orcsoundL)
        sound2 = random.choice(orcsoundL)
        while sound1 == sound2:
            sound2 = random.choice(orcsoundL)
        sound3 = random.choice(orcsoundL)
        while sound2 == sound3 or sound1 == sound3:
            sound3 = random.choice(orcsoundL)
    fname = "Va-"+str(sound1)+"-"+str(sound2)+"-"+str(sound3)
    mname  = "Gra-"+str(sound1)+"-"+str(sound2)+"-"+str(sound3)
    lname = "Zul-"+str(sound1)+"-"+str(sound2)+"-"+str(sound3)
    orcM.append(mname)
    orcF.append(fname)
    orcL.append(lname)


orcM.sort()
orcF.sort()
orcL.sort()

for i, j in enumerate(orcM):
    if (i>0) and orcM[i] == orcM[i-1]:
        orcM.remove(j)
for i, j in enumerate(orcF):
    if (i>0) and orcF[i] == orcF[i-1]:
        orcF.remove(j)
for i, j in enumerate(orcL):
    if (i>0) and orcL[i] == orcL[i-1]:
        orcL.remove(j)

for i in range(len(orcM)):
    name = orcM[i]
    orcnameM.write(name+"\n")
for i in range(len(orcF)):
    name = orcF[i]
    orcnameF.write(name+"\n")
for i in range(len(orcL)):
    name = orcL[i]
    orcnameL.write(name+"\n")
orcnameF.close()
orcnameM.close()
orcnameL.close()
    

