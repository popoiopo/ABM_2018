# model.py
from mesa_own.space import MultiGrid
from mesa_own import Model
from mesa_own.time import BaseScheduler
from mesa_own.datacollection import DataCollector

import random
import math
import numpy as np

from agents import *
from AStar import * 
from blocks import *


# ------------------Classes--------------------------
class Model(Model):
    '''
    ClubLife, an agent-based-model to simulate club related behaviour.
    '''
    def __init__(self, N, width, height,distance_coefficent,density_coefficent,density_vision ):
        super().__init__()

        self.max_Astar = 0
        self.num_agents = N

        self.partyRatio = .6
        self.maxAstar_pref = 35
        self.partyN = self.num_agents * self.partyRatio
        self.partyRest = self.num_agents - self.partyN
        self.dist_step = self.maxAstar_pref / self.partyRest



        self.grid = MultiGrid(width,height , False)
        self.schedule = BaseScheduler(self)
        self.POI_cost ={}
        self.grid_density = [ [0 for i in range(width)] for j in range(height)]

        self.serving_time = {'BAR': 3, 'BAR2':3, 'BAR3':3, 'BAR4': 3 }  


        POI_points = [ (24, 49),(40, 7), (5, 7), (40, 35), (5 ,35) ]
        #POI_points = [ (9, 33),(0, 5), (17, 5), (0,7),(17,7)]
        #POI_names = [ 'STAGE,'BAR1', 'BAR2','BAR3','BAR4']
        POI_names = ['STAGE', 'BAR', 'BAR2','BAR3','BAR4']
        POI_dict = {}
        for i in range(len(POI_points)):
            POI_dict[POI_names[i]] = POI_points[i]

        for i in range(width):
            for j in range(height):

                nd = nodeAgent((i, j), self, POI_names)
                self.grid.place_agent(nd, (i, j))

        self.blocks = block_positions
        create_block(self, block_positions, POI_names)


        create_POI(self,POI_points,2)

        for r in range(len(POI_points)):

            x = POI_points[r][0]
            y = POI_points[r][1]

            #A_star_node(self, (x, y), POI_names[r], self.blocks, 0.5, 2)
            self.POI_cost[POI_names[r]] =\
              A_star_array(width,height, (x, y), self.blocks, 0.5, 1)
       
        commuters_list = []
        for k in range(self.num_agents):
            a = commuterAgent(k, self, POI_dict, density_coefficent, density_vision)
            commuters_list.append(a)
             

        for commuter in commuters_list:

            self.schedule.add(commuter)

            notblock = False
            while(notblock is False):

                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                this_cell = self.grid.get_cell_list_contents((x, y))
                for agent in this_cell:

                    if type(agent) is nodeAgent:
                        if (agent.block is False):
                            notblock = True
                            break

            self.grid_density[x][y] +=  1
            self.grid.place_agent(commuter, (x, y))

        self.datacollector = DataCollector(
        #   model_reporters={"Gini": compute_gini},
            agent_reporters={"utility": lambda a: a.utility ,'numOfPOIVisits': lambda a: a.numOfPOIVisits})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
