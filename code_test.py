#This File only exists to test different code bits and pieces
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi*(N-i) for i,xi in enumerate(x))/(N*sum(x))
    return (1+(1/N)-2*B)

class MoneyAgent(Agent):
    #Agent with fixed start wealth
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center = False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth +=1
            self.wealth -=1
    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()
        #print("Agent "+str(self.unique_id)+" acted and has "+str(self.wealth)+" wealth.")

class MoneyModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        #Creator of Agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"})
        
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

model = MoneyModel(50, 10, 10)

for i in range(50):
    model.step()

agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
gini = model.datacollector.get_model_vars_dataframe()
gini.plot()
#plt.imshow(agent_counts, interpolation='nearest')
#plt.colorbar()
plt.show()

#while running == True:
#    model.step()
#    print("")
#    run +=1
#
#    if run == 20:
#        running = False
#        agent_wealth = [a.wealth for a in model.schedule.agents]
#        plt.hist(agent_wealth)
#        plt.show()
