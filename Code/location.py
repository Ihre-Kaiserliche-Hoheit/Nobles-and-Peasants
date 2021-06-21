class location():
    def __init__(self):
        self.uid = None
        self.name = ""

        self.size = 0
        self.x = 0
        self.y = 0

        self.inhabitans = []
        self.free_males = []
        self.free_females = []

        self.neighbors = [] #Links to all neighbors
        self.neighbor_uids = [] #UIDs of all neighbors

    def create(self, _input):
        self.uid = _input["ID"]
        self.name = _input["Name"]

        self.size = _input["size"]
        self.x = _input["x"]
        self.y = _input["y"]

        self.neighbor_uids = _input["Neighbors"]

    def update_free_lists(self):
        all = self.inhabitans
        free_males = list()
        free_females = list()
        for i in range(len(all)):
            person = all[i]
            if person.relations["spouse"] == None and 20 < person.age < 50:
                if person.isFemale == False:
                    free_males.append(person)
                else:
                    free_females.append(person)

    def update_inhabitans(self):
        all = self.inhabitans
        new_inhabitans = list()
        for i in range(len(all)):
            person = all[i]
            if person.isAlive == True:
                new_inhabitans.append(person)
        self.inhabitans = new_inhabitans
