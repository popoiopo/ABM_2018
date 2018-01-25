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

from mesa_own import Model
from mesa_own.space import MultiGrid
from mesa_own.datacollection import DataCollector

from agents import SsAgent, Sugar
from schedule import RandomActivationByBreed


class Sugarscape2ConstantGrowback(Model):
    """ A model simulating the dynamics within a danceclub. """
    verbose = True  # Print-monitoring

    def __init__(self, N, domain_size):
        '''
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        '''

        # Set parameters
        self.height = domain_size
        self.width = domain_size
        self.initial_population = N

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector({"SsAgent": lambda m: m.schedule.get_breed_count(SsAgent), })

        # Create sugar
        import numpy as np

        # Create agent:
        for i in range(self.initial_population):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            sugar = random.randrange(6, 25)
            metabolism = random.randrange(2, 4)
            vision = 1
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