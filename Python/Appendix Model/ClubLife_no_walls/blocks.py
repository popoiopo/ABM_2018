from ClubLife_no_walls.agents import *
from ClubLife_no_walls.model import *


# ------------------Functions--------------------------

def create_block(self, location_list, POI_locations):
    """
    This function takes a list of coordinates, and creates node agents of type block
    Args:
        locations_list :=   the list of block coordinates
        POI_locations :=    the model's dictionry that includes POI_names and their cooridantes 
    """

    
    for i in range(len(location_list)):
        this_cell = self.grid.get_cell_list_contents(location_list[i])

        for agent in this_cell:
            if type(agent) is nodeAgent:
                agent.block = True

                for i in POI_locations:
                    agent.locations[i] = 10000


def create_POI(self, location_list, moore_range):
    """
    This function takes a list of coordinates, and creates node agents of type  POI
    Args:
        locations_list :=   the list of POI coordinates
        moore_range := the moore_range for creating POIS
         (the range to add POIs around each coordinates in the location_list)
    """

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
                if not self.grid.out_of_bounds(coords):
                    this_cell = self.grid.get_cell_list_contents(coords)

                    for agent in this_cell:
                        if type(agent) is nodeAgent:

                            agent.POI = True


# ------------------variables--------------------------
block_positions = []

block_list = []

blocks = [item for sublist in block_list for item in sublist]

for b in blocks:
    block_positions.append(b)
