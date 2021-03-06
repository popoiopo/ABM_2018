import random
import math
from mesa_own import Agent
from ClubLife_no_walls.actions import *


# ------------------Classes--------------------------
class commuterAgent(Agent):
    """ This class model the commuter agents behaviors

    Attributes:
        state: the current state of the agent 
        layer: the current layer of agent
        WAITING_TIME_AT_POI: a counter that tracks the number of steps an agent waiting at a serviceable POI
        density_coefficent: defines the intensity or the preference of the agent in crowd avoidance
        vision_range: defines the Moore-range that agents are able to observe their environment
        POI_dict: A dictionary that holds the POI_names and their cooridnates
        shortest_time: it stores the shortest number of timesteps from the current poistion of the agent to
        its assigned POI
        total_waiting: tracks the number of timesteps  the agent spends upon its decision to move toward a POI
        unitl it reaches its POI
        numOfPOIVisits: stores the number of times agents visied serviceable POIs
        utility: stores the accumulated utility of the agents, as a value between 0-1, where 1 means that the agent
        visited their serviceable POIs within the shortest amount of time possible (calculated by A_star)
        util: used for sending utility value to Javascript function for visualization

    """
    def __init__(self, unique_id, model, POI_dict, density_coefficent, vision_range):
        super().__init__(unique_id, model)

        self.state = 'JUST_ARRIVED'
        self.layer = "STAGE"

        self.WAITING_TIME_AT_POI = 0
        self.density_coefficent = density_coefficent
        self.vision_range = vision_range

        self.POI_dict = POI_dict

        self.shortest_time = 0
        self.total_waiting = 0
        self.WaitingTime = 0
        self.numOfPOIVisits = 0
        self.utility = 0
        self.util = 0

    def move(self, destination):

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        cost_pos_list = []

        for k in possible_steps:
            x = k[0]
            y = k[1]
            cost_pos_list.append((self.model.POI_cost[destination][x][y], k))

        for k in range(len(cost_pos_list)):
            position = cost_pos_list[k][1]
            density = get_commuters_density(self, self.vision_range, position)
            cost_pos_list[k] = (cost_pos_list[k][0] + (self.density_coefficent * density /
                                math.pow(2 * (self.vision_range + 1) + 1, 2)), cost_pos_list[k][1])

        neighbor_list = self.model.grid.get_neighbors(self.pos, True, False, 1)

        for neighbor in neighbor_list:
            if type(neighbor) == commuterAgent and neighbor.layer == self.layer:
                for cost_pos_tuple in cost_pos_list:
                    if neighbor.pos == cost_pos_tuple[1]:
                        cost_pos_list = list(filter(lambda a: a != cost_pos_tuple, cost_pos_list))

        cost_pos_list.append((200, self.pos))
        best_cost = min(cost_pos_list, key=lambda x: x[0])[0]

        candidate_list = []

        for k in range(len(cost_pos_list)):
            if cost_pos_list[k][0] == best_cost:
                candidate_list.append(cost_pos_list[k][1])

        random.shuffle(candidate_list)
        new_position = candidate_list[0]
        if self.pos != new_position:
            self.model.grid_density[new_position[0]][new_position[1]] += 1
            self.model.grid_density[self.pos[0]][self.pos[1]] -= 1

        self.model.grid.move_agent(self, new_position)

    def step(self):
        getNextAction(self, self.state, self.POI_dict)


class nodeAgent(Agent):
    def __init__(self, pos, model, location_list):
        super().__init__(pos, model)
        self.locations = {}
        self.block = False
        self.POI = False
        for i in (location_list):
            self.locations[i] = -1

    def step(self):
        pass


# ------------------Functions--------------------------
def get_commuters_density(self, moore_range, position):

    x = position[0]
    y = position[1]

    agent_lst = []
    density = 0

    # repeated population
    grid_density = self.model.grid_density
    for i in range(1, moore_range):

        coordinates = []

        for j in range(2*i + 1):

            coordinates.append((x+i, y-i+j))
            coordinates.append((x-i, y-i+j))

        for k in range(1, 2*i):
            coordinates.append((x-i+k, y+i))
            coordinates.append((x-i+k, y-i))

        for coords in coordinates:
            if coords[0] < len(grid_density) and coords[1] < len(grid_density[0]) and\
               coords[0] >= 0 and coords[1] >= 0:

                density += grid_density[coords[0]][coords[1]]

    return density - 1
