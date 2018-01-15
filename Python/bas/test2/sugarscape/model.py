'''
Sugarscape Constant Growback Model
================================

Replication of the model found in Netlogo:
Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.
'''

import random
import numpy as np

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from sugarscape.agents import SsAgent, Sugar
from sugarscape.schedule import RandomActivationByBreed
from mesa.visualization.ModularVisualization import VisualizationElement


class Sugarscape2ConstantGrowback(Model):
    '''
    Sugarscape 2 Constant Growback
    '''

    verbose = True  # Print-monitoring

    def __init__(self, N, width, height):
        '''
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = N

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector({"SsAgent": lambda m: m.schedule.get_breed_count(SsAgent), })

        # Create sugar
        import numpy as np
        sugar_distribution = np.genfromtxt("sugarscape/sugar-map.txt")
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        # Create agent:
        for i in range(self.initial_population):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            sugar = random.randrange(6, 25)
            metabolism = random.randrange(2, 4)
            vision = random.randrange(1, 6)
            ssa = SsAgent((x, y), self, False, sugar, metabolism, vision)
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)

        self.running = True

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(SsAgent)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number Sugarscape Agent: ',
                  self.schedule.get_breed_count(SsAgent))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number Sugarscape Agent: ',
                  self.schedule.get_breed_count(SsAgent))


class HistogramModule(VisualizationElement):
    print("doe je het?!")
    package_includes = ["Chart.min.js"]
    local_includes = ["sugarscape/HistogramModule.js", "sugarscape/d3.min.js"]

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
        print(model.schedule.get_breed_count(SsAgent))
        # wealth_vals = [print(agent.SsAgent) for agent in model.schedule.agents]
        # hist = np.histogram(wealth_vals, bins=self.bins)[0]
        # return [int(x) for x in hist]

