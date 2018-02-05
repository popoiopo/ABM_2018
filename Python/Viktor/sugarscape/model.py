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

    def __init__(self, N, beta_c, beta_d, beta_w, beer_consumption, serving_speed, height=34, width=18, bar1_y = 21 , bar2_y = 21, stage = (9, 33)):
        '''
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = N
        self.bar1 = (0, bar1_y)
        self.bar1crowd = 0
        self.bar2 = (17,bar1_y)
        self.bar2crowd = 0
        self.bar3 = (0,bar2_y)
        self.bar3crowd = 0
        self.bar4 = (17,bar2_y)
        self.bar4crowd = 0
        self.stage = stage
        self.beta_c = beta_c
        self.beta_w = beta_w
        self.beta_d = beta_d
        self.beer_consumption = beer_consumption
        self.serving_speed = serving_speed
        self.WaitingTimes = []
        self.MaxAgents = 0

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)
        #self.datacollector = DataCollector({"SsAgent": lambda m: m.schedule.get_breed_count(SsAgent), })
        
        self.datacollector = DataCollector({"Waiting": lambda m: m.schedule.AverageWaitingTime(True), "MaxAgents": lambda m: m.schedule.MaxAgents()})

        # Create sugar
        import numpy as np

        
        # Create agent:
        for i in range(self.initial_population):
            #x = random.randrange(self.width)
            #y = random.randrange(self.height)
            
            x = 7 + int(5*np.random.random())
            y = 0
            vision = 2
            ssa = SsAgent((x, y), self,beta_c, beta_d, beta_w, beer_consumption, serving_speed, True, vision)
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)
        
        
        # sugar_distribution = np.genfromtxt("sugarscape/sugar-map.txt")
        sugar_distribution = np.zeros([self.width,self.height])
        for x in range(self.width):
            for y in range(self.height):
                sugar_distribution[x,y] = 0
    
    
        for _, x, y in self.grid.coord_iter():
            sugar = Sugar((x, y), self)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        self.running = True

    def WaitingTime(self, bar):
        busy = 0
        (x,y) = bar
        for dx in range(-4,5):
            for dy in range(-4,5):
                x_cor = x+dx
                y_cor = y+dy
                if 0 <= x_cor < self.width and 0 <= y_cor < self.height:
                    busy += len(self.grid.get_cell_list_contents([(x_cor,y_cor)]))
        return busy



    def step(self):
        self.WaitingTimes = []
        self.bar1crowd = self.WaitingTime(self.bar1)
        self.bar2crowd = self.WaitingTime(self.bar2)
        self.bar3crowd = self.WaitingTime(self.bar3)
        self.bar4crowd = self.WaitingTime(self.bar4)

        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(SsAgent)])

    def run_model(self, step_count=10):

        if self.verbose:
            print('Initial number Sugarscape Agent: ',
                  self.schedule.get_breed_count(SsAgent))
    
        for i in range(step_count):
            print(step_count)
            self.step()
        

        if self.verbose:
            print('')
            print('Final number Sugarscape Agent: ',
                  self.schedule.get_breed_count(SsAgent))


