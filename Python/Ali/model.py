# model.py
from mesa.space import MultiGrid
from mesa.space import SingleGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
import math
import sys
sys.setrecursionlimit(20000)



# (x+i,y-i+j,moore_range-i)
# (x-i,y-i+j,moore_range-i)
# (x-i+j,y+i,moore_range-i)
# (x-i+j,y-i,moore_range-i)


def A_star(self, location_point,location_name):

    pos = location_point
    node_list =[]
    check_list =[]

    neighbor_positions = self.grid.get_neighborhood(
            pos,
            moore=True,
            include_center=False)


    m_range = 1
    for i in range(len(neighbor_positions)):
            check_list.append(neighbor_positions[i])
            node_list.append((neighbor_positions[i],m_range))
            this_cell = self.grid.get_cell_list_contents(neighbor_positions[i])
            for agent in this_cell:
                    if type(agent) is nodeAgent:
                        if agent.locations[location_name] == -1:
                            agent.locations[location_name] = m_range 


    while(True):
        
        #find the neighbouring positions
        this_node = node_list.pop(0)
        pos = this_node[0]
        m_range = this_node[1]

        neighbor_positions = self.grid.get_neighborhood(
            pos,
            moore=True,
            include_center=False)
       
        #for each neighbouring positions, get the contents of that postion
        for i in range(len(neighbor_positions)):
            this_cell = self.grid.get_cell_list_contents(neighbor_positions[i])

            if not (neighbor_positions[i] in check_list ):
                node_list.append((neighbor_positions[i],m_range+1))
                check_list.append(neighbor_positions[i])
                # get the node agent, assign to its location value of i, which refers to the range of moor neighbourhood
                for agent in this_cell:
                    if type(agent) is nodeAgent:
                        if agent.locations[location_name] == -1:
                        
                            agent.locations[location_name] = m_range  
            


        if len(node_list) == 0:
            print(node_list)
            print(neighbor_positions)
            return
      
        #else:
        #    for p in range(len(neighbor_positions)):
        #        i += 1 
        #        A_star(self,neighbor_positions[p],location_name,i)


#define field agents (they hold info of closeness to POI,  )




class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        # Create agents
        #if math.pow((coords[0] - x),2) + math.pow( (coords[1]-y),2) <= math.pow(moore_range,2):


        #location_list ={'POI1','POI2','POI3'}
        location_list ={'POI2'}
        for i in range(height):
            for j in range(width):

               nd = nodeAgent((i,j),self,location_list)
               self.grid.place_agent(nd,(i,j))



        #locations =[(50,20),(50,80),(20,50)]
        #location_names =['POI1','POI2','POI3']
        locations = [(40,10)]
        location_names =['POI2']
        for r in range(len(locations)):
        #for r in range(3):    
            
            x= locations[r][0]
            y= locations[r][1]
            #x = random.randrange(self.grid.width)
            #y = random.randrange(self.grid.height)

            #locations.append((x,y))
        
            moore_range = 15
            for i in range(1,moore_range):
                for j in range(2*i+1):

                    for coords in [(x+i,y-i+j),\
                                   (x-i,y-i+j),\
                                   (x-i+j,y+i),\
                                   (x-i+j,y-i)]:
                        if math.pow((coords[0] - x),2) + math.pow( (coords[1]-y),2) <= math.pow(moore_range,2):
                            if  not self.grid.out_of_bounds(coords):          
                                poi = POIAgent(coords,self,moore_range-i)
                                self.grid.place_agent(poi, coords) 

        A_star(self, (x,y), location_names[r])                     


        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            #print(self.grid.get_cell_list_contents((x,y)))

            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": lambda a: a.wealth})


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)



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

class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #self.destination = random.choice(locations)
        self.wealth = 1

    def move(self,destination):

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        cost_pos_list = []
        candidate_list =[]
        for i in range(len(possible_steps)):
            
            this_cell = self.model.grid.get_cell_list_contents(possible_steps[i])
            for agent in this_cell:
                
                    if type(agent) is nodeAgent:
                    
                        if agent.locations[destination]:
                            cost_pos_list.append( (agent.locations[destination], possible_steps[i]) )
                            

        best_cost =min(cost_pos_list, key=lambda x:x[0])[0]
        #print(min(cost_pos_list, key=lambda x:x[0]))
        for k in range(len(cost_pos_list)):

            if cost_pos_list[k][0] ==  best_cost:
                candidate_list.append(cost_pos_list[k])
        
        random.shuffle(candidate_list)
     
        #new_position = random.choice(possible_steps)
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
        for i in (location_list):
            self.locations[i] = -1
             

    def step(self):
        pass
            


class POIAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self,pos,model,max_range):
        super().__init__(pos, model)
        self.wealth = max_range
        self.max_range = max_range
        
    def step(self):
        pass      


