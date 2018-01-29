from agents import *
from model import *

block_positions = []

def create_block(self, location_list, POI_locations):

    for i in range(len(location_list)):
            this_cell = self.grid.get_cell_list_contents(location_list[i])

            for agent in this_cell:
                if type(agent) is nodeAgent:
                    agent.block = True

                    for i in POI_locations:
                        agent.locations[i] = 10000000
                        						

block_list =[\
[(20 + i, 10) for i in range(10)],
[(20, 11), (20, 12), (20, 13), (20, 14)],
[(20 + i, 20) for i in range(10)],
[(20, 41), (20, 42), (20, 43), (20, 44)],
[(25, 20 + i) for i in range(10)],
[(25, 10 + i) for i in range(10)],
[(10, 0 + i) for i in range(10)],
[(0 + i, 30) for i in range(10)],
[(35 + i, 30) for i in range(10)],
[(15+i, 25) for i in range(10)]]


blocks = [item for sublist in block_list for item in sublist]

for b in blocks:
    block_positions.append(b)

