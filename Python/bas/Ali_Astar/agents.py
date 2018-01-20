import random
import math
from mesa import Agent


def get_distance(pos_1, pos_2):
    """ Get the distance between two point

    Args:
        pos_1, pos_2: Coordinate tuples for both points.

    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx ** 2 + dy ** 2)


class commuterAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self, destination):

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        cost_pos_list = [(100, self.pos)]

        for i in range(len(possible_steps)):

            this_cell = self.model.grid.get_cell_list_contents(possible_steps[i])
            for agent in this_cell:

                    if type(agent) is type(self):
                        break

                    if type(agent) is nodeAgent:

                        if agent.locations[destination]:
                            cost_pos_list.append((agent.locations[destination], possible_steps[i]))

        best_cost = min(cost_pos_list, key=lambda x: x[0])[0]
        candidate_list = []

        for k in range(len(cost_pos_list)):
            if cost_pos_list[k][0] == best_cost:
                candidate_list.append(cost_pos_list[k])
        neighbor_list = self.model.grid.get_neighbors(self.pos, True, False, 1)

        for neighbor in neighbor_list:
            if type(neighbor) == commuterAgent:
                for candidate in candidate_list:
                    if neighbor.pos in candidate:
                        candidate_list = list(filter(lambda a: a != candidate, candidate_list))

        random.shuffle(candidate_list)
        if candidate_list == []:
            return
        new_position = candidate_list[0][1]
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)

    def step(self):
        self.move('POI2')


class nodeAgent(Agent):
    def __init__(self, pos, model, location_list):
        super().__init__(pos, model)
        self.locations = {}
        self.block = False
        for i in (location_list):
            self.locations[i] = -1

    def step(self):
        pass


class POIAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, pos, model, max_range):
        super().__init__(pos, model)
        self.wealth = max_range
        self.max_range = max_range

    def step(self):
        pass
