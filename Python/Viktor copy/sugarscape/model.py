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

    def __init__(self, N, beta_c, beta_d, beta_w, beer_consumption, height=50, width=50, bar1 = (49, 40), bar2 = (49, 1), bar3 = (49, 18), bar4 = (0,18), stage = (24, 49)):
        '''
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = N
        self.bar1 = bar1
        self.bar2 = bar2
        self.bar3 = bar3
        self.bar4 = bar4
        self.stage = stage
        self.beta_c = beta_c
        self.beta_w = beta_w
        self.beta_d = beta_d
        self.beer_consumption = beer_consumption
        self.WaitingTimes = []

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        #self.datacollector = DataCollector({"SsAgent": lambda m: m.schedule.get_breed_count(SsAgent), })
        
        self.datacollector = DataCollector({"Waiting": lambda m: m.schedule.AverageWaitingTime(self.WaitingTimes, self.initial_population)})

        # Create sugar
        import numpy as np

        
        # Create agent:
        for i in range(self.initial_population):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            sugar = random.randrange(6, 25)
            metabolism = random.randrange(2, 4)
            vision = 2
            toilet_need = np.random.random()
            ssa = SsAgent((x, y), self,beta_c, beta_d, beta_w, beer_consumption, True, sugar, metabolism, vision)
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)
        
        
        # sugar_distribution = np.genfromtxt("sugarscape/sugar-map.txt")
        sugar_distribution = np.zeros([self.height,self.width])
        for x in range(self.width):
            for y in range(self.height):
                sugar_distribution[x,y] = 0
    
    
        for _, x, y in self.grid.coord_iter():
            sugar = Sugar((x, y), self)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        self.running = True

    def step(self):
        self.WaitingTimes = []
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
