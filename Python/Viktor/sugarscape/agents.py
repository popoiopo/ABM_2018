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


class SsAgent(Agent):
    def __init__(self, pos, model, moore=True, sugar=0, metabolism=0, vision=0):
        super().__init__(pos, model)
        self.pos = pos
        self.model = model
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision

    def get_sugar(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent

    def is_occupied(self, pos):
    
        # All 1st neighbors
        
        (x,y) = pos
        pos1 = (x+1,y)
        pos2 = (x+1,y+1)
        pos3 = (x+1,y-1)
        pos4 = (x-1,y)
        pos5 = (x-1,y+1)
        pos6 = (x-1,y-1)
        pos7 = (x,y+1)
        pos8 = (x,y-1)
        
        if x == 0:
            pos4 = (x+1,y)
            pos5 = (x+1,y)
            pos6 = (x+1,y)
        
        elif x == (self.model.width-1):
            pos1 = (x-1,y)
            pos2 = (x-1,y)
            pos3 = (x-1,y)
        
        if y == 0:
            pos3 = (x,y+1)
            pos6 = (x,y+1)
            pos8 = (x,y+1)
        
        elif y == (self.model.height-1):
            pos2 = (x,y-1)
            pos5 = (x,y-1)
            pos7 = (x,y-1)
    
        this_cell = self.model.grid.get_cell_list_contents([pos,pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8])
        
        return len(this_cell)


    def move(self):
    
        # Get neighborhood within vision
        (x,y) = self.pos
        neighbors = []
        
        for dx in range(-self.vision,self.vision+1):
            for dy in range(-self.vision,self.vision+1):
                if x+dx >= 0 and x+dx < self.model.width and y+dy >= 0 and y+dy < self.model.height:
                    pos = (x+dx,y+dy)
                    if abs(dx) > 1 or abs(dy) > 1:
                        if self.is_occupied(pos) == 0:
                            neighbors.append(pos)
                    else:
                        if self.is_occupied(pos) == 1:
                            neighbors.append(pos)
    
        neighbors.append(self.pos)
        
        # Find best place to go
        def score(pos):
            podiumwidth = 10
            x,y = pos
            if abs(x-((self.model.width-1)/2)) < podiumwidth:
                xpod = (self.model.width-1)/2
            else:
                xpod = x
            #score = (y)**2 + ((self.model.width-1)/2 - abs(xpod - (self.model.width-1)/2))**2
            score = (1.5*abs(y-99))**2 + abs(xpod-49.5)**2
            return score
        
        # Choose best place
        if len(neighbors) == 1:
            final_candidates = neighbors
        else:
            best_score =  min([score(pos) for pos in neighbors])
            candidates = [pos for pos in neighbors if score(pos)==
                    best_score]
            min_dist = min([get_distance(self.pos, pos) for pos in candidates])
            final_candidates = [pos for pos in candidates if get_distance(self.pos,
                pos) == min_dist]
        
            random.shuffle(final_candidates)
        
        self.model.grid.move_agent(self, final_candidates[0])



    def step(self):
        self.move()




class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = self.max_sugar
