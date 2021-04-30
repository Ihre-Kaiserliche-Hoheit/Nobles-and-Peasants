import file_code as fc


class converter():
    def __init__(self):
        print("Start conversion...")
        gedcom = open("gedcom.ged", "w+", newline="")
        raw_input = open("raw_output.txt", "r", newline="")
        gedcom.write("0 HEAD \n"
                     "1 SOUR PAF\n"
                     "2 VERS 2.1\n"
                     #"1 DESR ANSTFILE\n"
                     "1 SUBM @1@\n"
                     "1 SUBN @1@\n"
                     "1 GEDC\n"
                     "2 VERS 5.5\n"
                     "2 FORM Lineage-Linked\n"
                     "1 CHAR UTF-8\n\n")
        self.family_count = 1
        self.taken = []
        self.read_input(raw_input, gedcom)

    def read_input(self, file, gedcom):
        print("Read file...")
        raw_input = fc.txt_to_list("raw_output.txt")
        raw_input.pop(0)
        raw_input.pop(0)
        self.family_count = len(raw_input) + 1
        self.convertion(raw_input, gedcom)

    def convertion(self, raw_input, gedcom):
        print("Convert to .ged...")
        for i in range(len(raw_input)):
            indi = raw_input[i]
            indi = indi.split(";")
            
            indiID = indi[0]
            name = indi[1]
            surname = indi[2]
            if indi[3] == "0":
                sex = "M"
                husb = indiID
                wife = indi[6]
            else:
                sex = "F"
                wife = indiID
                husb = indi[6]
            fatherID = indi[4]
            motherID = indi[5]
            spouseID = indi[6]
            
            if 0 < len(indi[7]):
                children = self.strip_child(indi[7])

            birth = indi[8]
            if int(birth) < 100:
                birth = "0"+birth
            
            death = indi[9]
            if death != "None":
                if int(death) < 100:
                    death = "0"+death
            
        
            self.taken.append(indiID)
            familyID = self.family_count
            
            try:
                if self.taken.index(spouseID) == True:
                    pass

            except ValueError:
                self.add_fam_entry(familyID, husb, wife, children, gedcom)

            self.add_indi_entry(indiID, name, surname, sex, fatherID, motherID, spouseID, birth, death, familyID, gedcom)
    
        gedcom.close()
        print("Conversion finished!")

    def strip_child(self, children):
        children = children.strip("[")
        children = children.strip("]")
        children = children.strip(" ")
        children = children.split(",")

        kids = []

        for i in range(len(children)):
            child = children[i]
            if child != "":
                child = int(child)
                kids.append(child)
                
        return(kids)


    def add_indi_entry(self, indiID, name, surname, sex, fatherID, motherID, spouseID, birth, death, familyID, gedcom):
        gedcom.write("0 @"+str(indiID)+"@ INDI\n")
        gedcom.write("1 NAME "+str(name)+"/"+str(surname)+"/\n")
        gedcom.write("1 SEX "+str(sex)+"\n")
        gedcom.write("1 BIRT \n")
        gedcom.write("2 DATE "+str(birth)+"\n")
        if death != "None":
            gedcom.write("1 DEAT \n")
            gedcom.write("2 DATE "+str(death)+"\n")
        gedcom.write("1 FAMS @"+str(familyID)+"@\n") 
        gedcom.write("\n")
        

    def add_fam_entry(self, familyID, husb, wife, children, gedcom):
        gedcom.write("0 @"+str(familyID)+"@ FAM\n")
        if husb != "":
            gedcom.write("1 HUSB @"+str(husb)+"@\n")
        if wife != "":
            gedcom.write("1 WIFE @"+str(wife)+"@\n")
        if 0 < len(children):
            for i in range(len(children)):
                child = children[i]
                gedcom.write("1 CHIL @"+str(child)+"@\n") 
        self.family_count +=1
        gedcom.write("\n")
        pass
