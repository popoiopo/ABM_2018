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

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from sugarscape.agents import SsAgent, Sugar
from sugarscape.schedule import RandomActivationByBreed


class Sugarscape2ConstantGrowback(Model):
    '''
    Sugarscape 2 Constant Growback
    '''

    verbose = True  # Print-monitoring

    def __init__(self, height=100, width=100,
                 initial_population=500):
        '''
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = initial_population

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector({"SsAgent": lambda m: m.schedule.get_breed_count(SsAgent), })

        # Create sugar
        import numpy as np
        # sugar_distribution = np.genfromtxt("sugarscape/sugar-map.txt")
        """sugar_distribution = np.zeros([self.height,self.width])
        for x in range(self.width):
            for y in range(self.height):
                sugar_distribution[x,y] = (y/(49/7)) + ((25-abs(25-x))/8)
    
    
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)
        """
        # Create agent:
        for i in range(self.initial_population):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            sugar = random.randrange(6, 25)
            metabolism = random.randrange(2, 4)
            vision = 5
            ssa = SsAgent((x, y), self, True, sugar, metabolism, vision)
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
