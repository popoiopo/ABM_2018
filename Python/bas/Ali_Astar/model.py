# model.py
from mesa_own.space import MultiGrid
from mesa_own.space import SingleGrid
from mesa_own import Agent, Model
from mesa_own.time import RandomActivation
from mesa_own.datacollection import DataCollector
import random
import math
import sys
import numpy as np
from agents import *
sys.setrecursionlimit(20000)

# (x+i,y-i+j,moore_range-i)
# (x-i,y-i+j,moore_range-i)
# (x-i+j,y+i,moore_range-i)
# (x-i+j,y-i,moore_range-i)

def A_star(self, location_point, location_name, blocks):

    pos = location_point
    node_list = []
    check_list = []

    neighbor_positions = self.grid.get_neighborhood(
            pos,
            moore=True,
            include_center=False)

    m_range = 1
    for i in range(len(neighbor_positions)):
            check_list.append(neighbor_positions[i])
            node_list.append((neighbor_positions[i], m_range))
            this_cell = self.grid.get_cell_list_contents(neighbor_positions[i])
            for agent in this_cell:
                    if type(agent) is nodeAgent:
                        if agent.block is False and agent.locations[location_name] == -1:
                            dist = get_distance(location_point,neighbor_positions[i])

                            agent.locations[location_name] = m_range + 0.5 * dist

    while(True):

        # find the neighbouring positions
        this_node = node_list.pop(0)
        pos = this_node[0]
        m_range = this_node[1]

        neighbor_positions = self.grid.get_neighborhood(
            pos,
            moore=True,
            include_center=False)

        # for each neighbouring positions, get the contents of that postion
        for i in range(len(neighbor_positions)):
            this_cell = self.grid.get_cell_list_contents(neighbor_positions[i])

            if not (neighbor_positions[i] in check_list) and neighbor_positions[i] not in blocks:

                node_list.append((neighbor_positions[i],m_range+1))
                check_list.append(neighbor_positions[i])
                # get the node agent, assign to its location value of i, which refers to the range of moor neighbourhood
                for agent in this_cell:
                    if type(agent) is nodeAgent:
                        if agent.block is False and agent.locations[location_name] == -1:

                            dist = get_distance(location_point, neighbor_positions[i])
                            agent.locations[location_name] = m_range + 0.5 * dist

        if len(node_list) == 0:
            return


def create_block(self, location_list,):

    for i in range(len(location_list)):
            this_cell = self.grid.get_cell_list_contents(location_list[i])
            for agent in this_cell:

                if type(agent) is nodeAgent:
                        agent.block = True
                        for i in ['POI2']:
                            agent.locations[i] = 100000


class Model(Model):
    '''
    ClubLife, an agent-based-model to simulate club related behaviour.
    '''
    def __init__(self, N, domain_size):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(domain_size, domain_size, False)
        self.schedule = RandomActivation(self)

        # location_list = {'POI1','POI2','POI3'}
        location_list ={'POI2'}
        for i in range(domain_size):
            for j in range(domain_size):

                nd = nodeAgent((i, j), self, location_list)
                self.grid.place_agent(nd, (i, j))

        locations = [(40, 10)]
        location_names = ['POI2']
        for r in range(len(locations)):
        # for r in range(3):

            x = locations[r][0]
            y = locations[r][1]

            moore_range = 5
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

        block1 = [(20 + i, 10) for i in range(10)]
        block2 = [(20, 11), (20, 12), (20, 13), (20, 14)]
        block3 = [(20 + i, 20) for i in range(10)]
        block4 = [(20, 41), (20, 42), (20, 43), (20, 44)]
        block5 = [(25, 20 + i) for i in range(10)]
        block6 = [(25, 10 + i) for i in range(10)]
        block7 = [(10, 0 + i) for i in range(10)]
        block8 = [(0 + i, 30) for i in range(10)]
        block9 = [(35 + i, 30) for i in range(10)]

        blocks = []
        for b in [block1, block2, block3, block4, block5, block6, block7, block8, block9]:
            for e in b:
                blocks.append(e)

        create_block(self, blocks)

        A_star(self, (x, y), location_names[r], blocks)

        for i in range(self.num_agents):
            a = commuterAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            # print(self.grid.get_cell_list_contents((x,y)))

            self.grid.place_agent(a, (x, y))

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},
        #     agent_reporters={"Wealth": lambda a: a.wealth})

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
