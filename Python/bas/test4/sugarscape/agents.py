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
        (x,y) = pos
        pos1 = (x+1,y)
        pos2 = (x-1,y)
        pos3 = (x,y+1)
        pos4 = (x,y-1)
        
        if x == 0:
            pos2 = (x+1,y)
        elif x == (self.model.width-1):
            pos1 = (x-1,y)
        if y == 0:
            pos4 = (x,y+1)
        elif y == (self.model.height-1):
            pos3 = (x,y-1)
    
        this_cell = self.model.grid.get_cell_list_contents([pos,pos1, pos2, pos3, pos4])
        return len(this_cell) > 1


    def move(self):
        # Get neighborhood within vision
        (x,y) = self.pos
        neighbors = []
        for dx in range(-1,2):
            for dy in range(-1,2):
                if x+dx >= 0 and x+dx < self.model.width and y+dy >= 0 and y+dy < self.model.height:
                    pos = (x+dx,y+dy)
                    #if dx == 0 or dy == 0
                    if not self.is_occupied(pos):
                        neighbors.append(pos)
        neighbors.append(self.pos)
        # Find best place to go
        def score(pos):
            x,y = pos
            if abs(x-((self.model.width-1)/2)) < 10:
                xpod = (self.model.width-1)/2
            else:
                xpod = x
            score = 1.5*y + (self.model.width-1)/2 - abs(xpod - (self.model.width-1)/2)
            return score
        
        if len(neighbors) == 1:
            final_candidates = neighbors
        else:
            best_score =  max([score(pos) for pos in neighbors[:-1]])
            candidates = [pos for pos in neighbors if score(pos)==
                    best_score]
            min_dist = min([get_distance(self.pos, pos) for pos in candidates])
            final_candidates = [pos for pos in candidates if get_distance(self.pos,
                pos) == min_dist]
        
            random.shuffle(final_candidates)
        
        self.model.grid.move_agent(self, final_candidates[0])

        #self.model.grid.move_agent(self, candidate[0])
    
    
    def move2(self):
        # Get neighborhood within vision
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, False,
                False, radius=self.vision) if not self.is_occupied(i)]
        neighbors.append(self.pos)
        # Look for location with the most sugar
        max_sugar = max([self.get_sugar(pos).amount for pos in neighbors])
        candidates = [pos for pos in neighbors if self.get_sugar(pos).amount ==
                max_sugar]
        
        # Narrow down to the nearest ones
        min_dist = min([get_distance(self.pos, pos) for pos in candidates])
        final_candidates = [pos for pos in candidates if get_distance(self.pos,
            pos) == min_dist]
        
        random.shuffle(final_candidates)
        
        self.model.grid.move_agent(self, final_candidates[0])

    def eat(self):
        (x,y) = self.pos
        if x != 0:
            self.left= (x-1,y)
        else:
            self.left = (x+1,y)
        if x != 49:
            self.right = (x+1,y)
        else:
            self.right = (x-1,y)
        if y != 49:
            self.up = (x,y+1)
        else:
            self.up = (x, y-1)
        if x != 49:
            sugar_patch_right = self.get_sugar(self.right)
            sugar_patch_right.amount = 0
        if x != 0:
            sugar_patch_left = self.get_sugar(self.left)
            sugar_patch_left.amount = 0
        if y != 49:
            sugar_patch_up = self.get_sugar(self.up)
            sugar_patch_up.amount = 0
    
    def restore(self):
        (x,y) = self.pos
        if x != 0:
            self.left= (x-1,y)
        else:
            self.left = (x+1,y)
        if x != 49:
            self.right = (x+1,y)
        else:
            self.right = (x-1,y)
        if y != 49:
            self.up = (x,y+1)
        else:
            self.up = (x, y-1)
        if x != 49:
            sugar_patch_right = self.get_sugar(self.right)
            sugar_patch_right.amount = sugar_patch_right.max_sugar
        if x != 0:
            sugar_patch_left = self.get_sugar(self.left)
            sugar_patch_left.amount = sugar_patch_left.max_sugar
        if y != 49:
            sugar_patch_up = self.get_sugar(self.up)
            sugar_patch_up.amount = sugar_patch_up.max_sugar

    def step(self):
        #self.restore()
        self.move()
        #self.eat()



class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = self.max_sugar
