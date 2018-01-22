import random
import math
import numpy as np
from mesa import Agent
from schedule import *


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

def get_commuters_density(self,moore_range,position):

    x= position[0]
    y= position[1]

    agent_lst =[]
    #repeated population 
    for i in range(1,moore_range):
        for j in range(2*i+1):

            for coords in [(x+i,y-i+j),\
                           (x-i,y-i+j),\
                           (x-i+j,y+i),\
                           (x-i+j,y-i)]:
                if math.pow((coords[0] - x),2) + math.pow( (coords[1]-y),2) <= math.pow(moore_range,2):
                    if  not self.model.grid.out_of_bounds(coords):
                        cell_content =  self.model.grid.get_cell_list_contents(coords)
                        for k in cell_content:
                           
                            if type(k) == commuterAgent:
                                agent_lst.append(k.unique_id)

    return len(list(set(agent_lst)))                       







class commuterAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model,destination):
        super().__init__(unique_id, model)

        self.density_coefficent = 3
        self.destination =  destination

    def move(self,destination):

        cost_pos_list = []

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            True,
            False,1)
       
        for i in range(len(possible_steps)):
            
            this_cell = self.model.grid.get_cell_list_contents(possible_steps[i])

            for agent in this_cell:

                    #if type(agent) is type(self):
                    #    break
                        
                    if type(agent) is nodeAgent:
                    
                        if agent.locations[destination]:
                            cost_pos_list.append( (agent.locations[destination], possible_steps[i]) )

                                     
            for k in range(len(cost_pos_list)):
                position = cost_pos_list[k][1]
        
                density = get_commuters_density(self,2,position)

                cost_pos_list[k] = (cost_pos_list[k][0] + ( self.density_coefficent * density / self.model.num_agents )\
                                     , cost_pos_list[k][1])

        neighbor_list = self.model.grid.get_neighbors(self.pos, True, False, 1)

        for neighbor in neighbor_list:
            if type(neighbor) == commuterAgent:
                for cost_pos_tuple in cost_pos_list:
                    if neighbor.pos == cost_pos_tuple[1]:
                        cost_pos_list = list(filter(lambda a: a != cost_pos_tuple, cost_pos_list))



        cost_pos_list.append((200,self.pos))
        best_cost = min(cost_pos_list, key=lambda x:x[0])[0]
        candidate_list =[]

        #candidate_list = sorted([candidate_list, key=lambda x: x[0])                

        for k in range(len(cost_pos_list)):
            if cost_pos_list[k][0] == best_cost:
                candidate_list.append(cost_pos_list[k][1]) 

       
        random.shuffle(candidate_list)
        new_position = candidate_list[0]
        self.model.grid.move_agent(self, new_position)


    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)


    def step(self):
        self.move(self.destination)
  


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
    def __init__(self,pos,model,m_range):
        super().__init__(pos, model)
        self.gradient = m_range
        
    def step(self):
        pass      
