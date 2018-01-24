import random
import math
from mesa_own import Agent

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


def get_commuters_density(self, moore_range, position):

    x = position[0]
    y = position[1]

    agent_lst = []
    # repeated population
    for i in range(1, moore_range):
        for j in range(2*i+1):

            for coords in [(x+i, y-i+j),
                           (x-i, y-i+j),
                           (x-i+j, y+i),
                           (x-i+j, y-i)]:
                if math.pow((coords[0] - x), 2) + math.pow((coords[1]-y), 2) <= math.pow(moore_range, 2):
                    if not self.model.grid.out_of_bounds(coords):
                        cell_content = self.model.grid.get_cell_list_contents(coords)
                        for k in cell_content:

                            if type(k) == commuterAgent:
                                agent_lst.append(k.unique_id)

    return len(list(set(agent_lst)))


class commuterAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, destination):
        super().__init__(unique_id, model)
        self.state = 'JUST_ARRIVED'
        self.action = 'DO_NOTHING'
        self.WAITING_TIME_AT_BAR =0
        self.WAITING_TIME_AT_WC = 0
        self.density_coefficent = 0
        self.POI_dict = {'STAGE': (26, 49),'BAR': (40, 10), 'WC': (5, 7)}

        self.destination = destination

    def move(self, destination):

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)


        cost_pos_list = []

        for i in range(len(possible_steps)):

            this_cell = self.model.grid.get_cell_list_contents(possible_steps[i])
            for agent in this_cell:

                    # if type(agent) is type(self):
                    #     break

                    if type(agent) is nodeAgent:

                        if agent.locations[destination]:
                            cost_pos_list.append((agent.locations[destination], possible_steps[i]))

            for k in range(len(cost_pos_list)):
                position = cost_pos_list[k][1]
                density = get_commuters_density(self, 2, position)
                cost_pos_list[k] = (cost_pos_list[k][0] + (self.density_coefficent * density / self.model.num_agents), cost_pos_list[k][1])

        neighbor_list = self.model.grid.get_neighbors(self.pos, True, False, 1)

        # if self.unique_id == 1:
        #     print("########################################")
        #     print(self.unique_id)
        #     print(self.pos)

        for neighbor in neighbor_list:
            if type(neighbor) == commuterAgent:
                for cost_pos_tuple in cost_pos_list:
                    if neighbor.pos == cost_pos_tuple[1]:
                        cost_pos_list = list(filter(lambda a: a != cost_pos_tuple, cost_pos_list))

        cost_pos_list.append((200, self.pos))
        # if self.unique_id == 1:
        #     print(cost_pos_list)
        best_cost = min(cost_pos_list, key=lambda x: x[0])[0]
        candidate_list = []

        # candidate_list = sorted([candidate_list, key=lambda x: x[0])

        for k in range(len(cost_pos_list)):
            if cost_pos_list[k][0] == best_cost:
                candidate_list.append(cost_pos_list[k][1])

        random.seed(5)
        random.shuffle(candidate_list)
        new_position = candidate_list[0]
        # if self.unique_id == 1:
        #     print(candidate_list)
        #     for i in cost_pos_list:
        #         if new_position in i:
        #             print(i)
        self.model.grid.move_agent(self, new_position)


    def getNextAction(self, state,POI_dict):

        state = self.state
        action = self.action

        if state == 'JUST_ARRIVED':

            possible_actions = ['GO_TO_STAGE','GO_TO_WC','GO_TO_BAR']
            possible_actions_probablities = [0.9,0.05, 0.05]

            rand =random.random()
            if rand <= 0.9 :

                state = 'MOVING_TO_STAGE'
                action = 'GO_TO_STAGE'
                self.move('STAGE')

            elif  (rand > 0.9 and rand <= (0.9 + 0.05)  ):
                    
                state = 'MOVING_TO_WC'
                action = 'GO_TO_WC'
                self.move('WC')

            else:

                state ='MOVING_TO_BAR'
                action = 'GO_TO_BAR'
                self.move('BAR')


        if state == 'BEING_AT_BAR':

            if self.WAITING_TIME_AT_BAR <= 5:

                self.WAITING_TIME_AT_BAR += 1
                action = 'DO_NOTHING'

            else:

                self.WAITING_TIME_AT_BAR  = 0
                state = 'MOVING_TO_STAGE'
                self.move('STAGE')

            
        if state == 'BEING_AT_WC':

            if self.WAITING_TIME_AT_WC <= 5:

                self.WAITING_TIME_AT_WC += 1
                action = 'DO_NOTHING'

            else:

                self.WAITING_TIME_AT_WC = 0
                state = 'MOVING_TO_STAGE'
                self.move('STAGE')


        if state == "MOVING_TO_STAGE":

            action = 'GO_TO_STAGE'
            self.move('STAGE')

            effort_distance =(10,1000)
        # here we will have inner states at stage, for example try to get closer, if they see empty spaces   

            # TO DO HOW to place the agents when they arrive
            if get_distance(self.pos,POI_dict['STAGE']) <= 7:
                state = "BEING_AT_STAGE"
            #else:
            # try to get closer to location, in 5 attempts, otherwise, 
            # change state to AT stage, and record your happiness, by your distance from stage.     


        if state == 'MOVING_TO_BAR':

            action = 'GO_TO_BAR'
            self.move('BAR')


        if state== 'MOVING_TO_WC':

            action = 'GO_TO_WC'
            self.move('WC')


        if state == 'BEING_AT_STAGE':

            possible_actions = ['DO_NOTHING','GO_TO_BAR','GO_TO_WC']
            possible_actions_probablities = [0.8, 0.15, 0.05]

            rand = random.random()
            if rand <= 0.8:

                action = 'DO_NOTHING'

            elif  (rand > 0.8 and  rand <= (0.8 + 0.15) ):

                action = 'GO_TO_BAR'
                state = 'moveing_toward_Bar'
                self.move('BAR')

            else: 

                action = 'GO_TO_WC'
                state = 'MOVING_TO_WC'
                self.move('WC')

        self. state = state
        self. action = action

        return (state, action) 


    def step(self):

        if self.unique_id == 1:
             print("########################################")
             print(self.unique_id)
             print(self.pos)
             #print(self.getNextAction(self.state,self.POI_dict))
       
        self.getNextAction(self.state,self.POI_dict)
        #self.move(self.destination)


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
