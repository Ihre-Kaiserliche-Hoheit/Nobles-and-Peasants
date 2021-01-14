#TODO:
# Currently Nothing

class converter():
    def __init__(self):
        gedcom = open("gedcom.ged", "w+", newline="")
        input_file = open("save_file.csv", "r", newline="")
        gedcom.write("0 HEAD \n")
        gedcom.write("1 SOUR PAF \n")
        gedcom.write("2 VERS 2.1 \n")
        gedcom.write("1 DESR ANSTFILE \n")
        gedcom.write("1 SUBM @5@ \n")
        gedcom.write("1 SUBN @8@ \n")
        gedcom.write("1 GEDC \n")
        gedcom.write("2 VERS 5.4 \n")
        gedcom.write("2 FORM Lineage-Linked \n")
        gedcom.write("1 CHAR UTF-8 \n \n")
        self.fcount = 1
        self.taken = []
        self.read_input(input_file, gedcom)

    def read_input(self, input_file, gedcom):
        input_list = input_file.read().splitlines()
        input_file.close()
        input_file = input_list
        del(input_list)
        input_file.pop(0)
        self.convert_fam(input_file, gedcom)

    def convert_fam(self, input_file, gedcom):
        for i in range(len(input_file)):
            indi = input_file[i]
            indi = indi.split(";") #Cuts the string into nice little pieces
            indiid = indi[0]
            firstname = indi[1]
            #Chose what the lastname will be
            if indi[3] == "" and indi[2] == "":
                lastname = ""
            elif indi[3] == "" and not indi[2] == "":
                lastname = indi[2]
            else:
                lastname = indi[3]
            #print(lastname)
            if indi[4] == "Male":
                sex = "M"
            elif indi[4] == "Female":
                sex = "F"
            else:
                sex = "Something is wrong, mate"
            bday = indi[8]
            bplace = ""
            dday = indi[9]
            dplace = ""
            cast = ""
            if indi[4] == "Male":
                sex = "M"
            elif indi[4] == "Female":
                sex = "F"
            else:
                sex = "Something is wrong, mate"
            spouse = indi[7]
            children = indi[11]
            if sex == "M":
                husb = indiid
                wife = spouse
            else:
                husb = spouse
                wife = indiid
            mday = ""
            mplace = ""
            if len(children) > 0:
                children = children.strip("[")
                children = children.strip("]")
                children = children.strip(" ")
                children = children.split(",")
                nc = []
                for ii in range(len(children)):
                    ce = children[ii]
                    if ce != "":
                        ce = int(ce)
                        nc.append(ce)
                children = nc
                del(nc)
                #print(children)
            self.taken.append(indi[0])
            spouse_found = False
            f = self.fcount
            for ii in range(len(self.taken)):
                j = self.taken[ii]
                if j == spouse:
                    spouse_found = True
            if spouse_found == False:     
                self.add_fam(self.fcount, husb, wife, children, mday, mplace, gedcom)
            self.add_indi(indiid, firstname, lastname, sex, bday, bplace, dday, dplace, cast, f, gedcom)
           
    def add_indi(self, indiid, firstname, surname, sex, bday, bplace, dday, dplace, cast, fam, gedcom):
        gedcom.write("0 @"+str(indiid)+"@ INDI\n")
        gedcom.write("1 NAME "+str(firstname)+"/"+str(surname)+"/ \n")
        gedcom.write("1 SEX "+str(sex)+"\n")
        gedcom.write("1 BIRT \n")
        gedcom.write("2 DATE "+str(bday)+"\n")
        if bplace != "":
            gedcom.write("2 PLAC "+str(bplace)+"\n")
        if dday != "":
            gedcom.write("1 DEAT \n")
            gedcom.write("2 DATE "+str(dday)+"\n")
            if dplace != "":
                gedcom.write("2 PLAC "+str(dplace)+"\n")
        gedcom.write("1 CAST "+str(cast)+"\n")
        gedcom.write("1 FAMS @"+str(fam)+"@ \n") 
        gedcom.write("\n")#LAST LINE

    def add_fam(self, fcount, husb, wife, children, mday, mplace, gedcom):
        gedcom.write("0 @"+str(fcount)+"@ FAM\n")
        if mday != "" and mplace != "":
            gedcom.write("1 MARR \n")
            if mday != "":
                gedcom.write("2 DATE "+str(mday)+"\n")
            if mplace != "":
                gedcom.write("2 PLAC "+str(mplace)+"\n")
        if husb != "":
            gedcom.write("1 HUSB @"+str(husb)+"@\n")
        if wife != "":
            gedcom.write("1 WIFE @"+str(wife)+"@\n")
        if len(children) > 0:
            #print("DEBUG CHILD ADDING")
            for i in range(len(children)):
                child = children[i]
                gedcom.write("1 CHIL @"+str(child)+"@ \n") 
        self.fcount = self.fcount+1
        gedcom.write("\n")#LAST LINE
        #print("A new family "+str(husb)+" "+str(wife))

    def end(self):
        gedcom.close()
