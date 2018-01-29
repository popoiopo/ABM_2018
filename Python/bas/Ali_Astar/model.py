# model.py
from mesa_own.space import MultiGrid
from mesa_own import Model
from mesa_own.time import BaseScheduler
from mesa_own.datacollection import DataCollector


import random
import math
import sys
import numpy as np
from agents import *
from AStar import * 


sys.setrecursionlimit(20000)

# (x+i,y-i+j,moore_range-i)
# (x-i,y-i+j,moore_range-i)
# (x-i+j,y+i,moore_range-i)
# (x-i+j,y-i,moore_range-i)



def create_block(self, location_list, POI_locations):

    for i in range(len(location_list)):
            this_cell = self.grid.get_cell_list_contents(location_list[i])

            for agent in this_cell:
                if type(agent) is nodeAgent:
                    agent.block = True

                    for i in POI_locations:
                        agent.locations[i] = 10000000000


class Model(Model):
    '''
    ClubLife, an agent-based-model to simulate club related behaviour.
    '''
    def __init__(self, N, domain_size):
        super().__init__()
        self.max_Astar = 0
        self.num_agents = N
        self.partyRatio = .6
        self.maxAstar_pref = 35
        self.partyN = self.num_agents * self.partyRatio
        self.partyRest = self.num_agents - self.partyN
        self.dist_step = self.maxAstar_pref / self.partyRest
        self.grid = MultiGrid(domain_size, domain_size, False)
        self.schedule = BaseScheduler(self)
        self.locations_cost ={}

        locations = [ (26, 49),(40, 10), (5, 7)]
        #location_names = ['POI1', 'POI2', 'POI3']
        location_names = ['STAGE', 'BAR', 'WC']

        for i in range(domain_size):
            for j in range(domain_size):

                nd = nodeAgent((i, j), self, location_names)
                self.grid.place_agent(nd, (i, j))

        block1 = [(20 + i, 10) for i in range(10)]
        block2 = [(20, 11), (20, 12), (20, 13), (20, 14)]
        block3 = [(20 + i, 20) for i in range(10)]
        block4 = [(20, 41), (20, 42), (20, 43), (20, 44)]
        block5 = [(25, 20 + i) for i in range(10)]
        block6 = [(25, 10 + i) for i in range(10)]
        block7 = [(10, 0 + i) for i in range(10)]
        block8 = [(0 + i, 30) for i in range(10)]
        block9 = [(35 + i, 30) for i in range(10)]
        block10 = [(15+i, 25) for i in range(10)]

        self.blocks = []
        for b in [block1, block2, block3, block5, block6, block7, block8, block9, block10]:
            for e in b:
                self.blocks.append(e)

        create_block(self, self.blocks, location_names)

        for r in range(len(locations)):

            x = locations[r][0]
            y = locations[r][1]

            moore_range = 1
            for i in range(1, moore_range):
                for j in range(2*i+1):

                    for coords in [(x+i, y-i+j),
                                   (x-i, y-i+j),
                                   (x-i+j, y+i),
                                   (x-i+j, y-i)]:
                        if math.pow((coords[0] - x), 2) + math.pow((coords[1] - y), 2) <= math.pow(moore_range, 2):
                            if not self.grid.out_of_bounds(coords):
                                poi = POIAgent(coords, self, moore_range-i)
                                self.grid.place_agent(poi, coords)

            A_star_node(self, (x, y), location_names[r], self.blocks, 0.5, 2)

            self.locations_cost[location_names[r]] =  A_star_array(domain_size,domain_size, (x, y), self.blocks, 0.5, 2)

        # array_plop = np.zeros((50, 50))
        # for i in range(50):
        #     for j in range(50):
        #         this_cell = self.grid.get_cell_list_contents((i, j))
        #         for agent in this_cell:
        #             if type(agent) is nodeAgent:
        #                  array_plop[49 - i][j] = agent.locations['POI1']

        # np.set_printoptions(precision=1)
        # for i in array_plop:
        #     print(i)
        # print(array_plop)
        # with open("Output.txt", "w") as text_file:
        #     for i in array_plop:
        #         text_file.write(str(i))

        commuters_list = []
        for k in range(self.num_agents):
            a = commuterAgent(k, self, location_names[0])
            # b = commuterAgent(agentId, self, location_names[0])
            # agentId += 1
            # c = commuterAgent(agentId, self, location_names[0])
            # agentId += 1
            commuters_list.append(a)
            # commuters_list.append(b)
            # commuters_list.append(c)

        for commuter in commuters_list:

            self.schedule.add(commuter)

            # Add the agent to a random grid cell
            notblock = False
            while(notblock is False):
                # random.seed(5)
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                this_cell = self.grid.get_cell_list_contents((x, y))
                for agent in this_cell:

                    if type(agent) is nodeAgent:
                        if (agent.block is False):
                            notblock = True
                            break

            self.grid.place_agent(commuter, (x, y))

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},
        #     agent_reporters={"Wealth": lambda a: a.wealth})

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
