# model.py
import random
import numpy as np
from mesa_own import Agent, Model
from mesa_own.time import RandomActivation
from mesa_own.space import MultiGrid
from mesa_own.datacollection import DataCollector
from mesa_own.batchrunner import BatchRunner

from mesa_own.visualization.ModularVisualization import VisualizationElement

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    print("&&*&*&(*(&*((&(*(")
    print(x, N, B, (1 + (1/N) - 2*B))
    return (1 + (1/N) - 2*B)


class MoneyModel(Model):
    """ A model with some number of agents. """
    def __init__(self, N, width, height):
        self.running = True
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={"Gini" : compute_gini},
            agent_reporters={"Wealth": lambda a: a.wealth}
        )

        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Add the agents on the grid
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        ''' Advance the model by one step. '''
        self.datacollector.collect(self)
        self.schedule.step()


class MoneyAgent(Agent):
    """ An agent with fixed initial wealth. """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        # The step of the agent
        self.move()
        if self.wealth > 0:
            self.give_money()

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js", "d3.min.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        wealth_vals = [agent.wealth for agent in model.schedule.agents]
        print(wealth_vals)
        hist = np.histogram(wealth_vals, bins=self.bins)[0]
        print(hist)
        print([int(x) for x in hist])
        return [int(x) for x in hist]
