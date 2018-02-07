from ClubLife.agents import *
from ClubLife.model import *


# ------------------Functions--------------------------

def create_block(self, location_list, POI_locations):

    for i in range(len(location_list)):
        this_cell = self.grid.get_cell_list_contents(location_list[i])

        for agent in this_cell:
            if type(agent) is nodeAgent:
                agent.block = True

                for i in POI_locations:
                    agent.locations[i] = 10000


def create_POI(self, location_list, moore_range):
    for r in range(len(location_list)):

        x = location_list[r][0]
        y = location_list[r][1]

        coordinates = []
        for i in range(moore_range):
            for j in range(moore_range):
                if x+i > 0 and len(self.grid_density) > x+i and y+j > 0\
                    and len(self.grid_density[0]) > y+j:

                        coordinates.append((x+i, y+j))
                        coordinates.append((x-i, y-j))
                        coordinates.append((x-i, y+j))
                        coordinates.append((x+i, y-j))

            for coords in coordinates:
                # if math.pow((coords[0] - x), 2) + math.pow((coords[1] - y), 2) <= math.pow(moore_range, 2):
                if not self.grid.out_of_bounds(coords):
                    this_cell = self.grid.get_cell_list_contents(coords)

                    for agent in this_cell:
                        if type(agent) is nodeAgent:

                            agent.POI = True


# ------------------variables--------------------------
block_positions = []

block_list = [[(25 + i, 25) for i in range(25)],
              [(0 + i, 25) for i in range(24)],
              [(1 + i, 27) for i in range(48)]]

blocks = [item for sublist in block_list for item in sublist]

for b in blocks:
    block_positions.append(b)
