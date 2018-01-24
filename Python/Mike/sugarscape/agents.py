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
    def __init__(self, pos, model, moore=True, sugar=0, metabolism=0, vision=0, count=0, thirst=False, pee=False, queue = False):
        super().__init__(pos, model)
        self.pos = pos
        self.model = model
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        self.count = count 
        self.countp = count
        self.thirst = thirst
        self.queue = queue
        self.pee = pee
        self.blatter = random.randint(0,10)
        self.consumption = random.randint(0,10)

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
        #print(this_cell, "deze cellaaaaa")
        return len(this_cell)


    def move(self):
    
        # Get neighborhood within vision
        (x,y) = self.pos
        neighbors = []
        
        for dx in range(-self.vision,self.vision+1):
            for dy in range(-self.vision,self.vision+1):
                if x+dx >= 0 and x+dx < self.model.width and y+dy >= 0 and y+dy < self.model.height:
                    pos = (x+dx,y+dy)
                    if self.thirst == False and self.pee == False:
                        if abs(dx) > 1 or abs(dy) > 1:
                            if self.is_occupied(pos) == 0:
                                neighbors.append(pos)
                        else:
                            if self.is_occupied(pos) == 1:
                                neighbors.append(pos)
                    if self.thirst == True or self.pee == True:
                        if abs(dx) > 1 or abs(dy) > 1:
                            if self.is_occupied(pos) == 0:
                                neighbors.append(pos)
                        else:
                            if self.is_occupied(pos) != 1:
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
            score_bar = -x+y
            score_pee = x+y
            return score, score_bar, score_pee
        
        # Choose best place
        if self.thirst == False and self.pee == False:
            if len(neighbors) == 1:
                final_candidates = neighbors
            else:
                best_score =  min([score(pos)[0] for pos in neighbors])
                candidates = [pos for pos in neighbors if score(pos)[0]==
                        best_score]
                min_dist = min([get_distance(self.pos, pos) for pos in candidates])
                final_candidates = [pos for pos in candidates if get_distance(self.pos,
                    pos) == min_dist]

                random.shuffle(final_candidates)

        if self.thirst == True and self.pee == False:
            if len(neighbors) == 1:
                final_candidates = neighbors
            else:
                best_score =  min([score(pos)[1] for pos in neighbors])
                candidates = [pos for pos in neighbors if score(pos)[1]==
                        best_score]
                min_dist = min([get_distance(self.pos, pos) for pos in candidates])
                final_candidates = [pos for pos in candidates if get_distance(self.pos,
                    pos) == min_dist]
        
                random.shuffle(final_candidates)
                print(final_candidates[0], best_score)
                if best_score < -80:
                    self.thirst = False
                    self.count = 0
                    self.queue = True
                    print('ik sta in de rij')

        if self.pee == True:
            if len(neighbors) == 1:
                final_candidates = neighbors
            else:
                best_score =  min([score(pos)[2] for pos in neighbors])
                candidates = [pos for pos in neighbors if score(pos)[2]==
                        best_score]
                min_dist = min([get_distance(self.pos, pos) for pos in candidates])
                final_candidates = [pos for pos in candidates if get_distance(self.pos,
                    pos) == min_dist]
                print(best_score, "pee")
        
                random.shuffle(final_candidates)
                print(final_candidates[0], best_score)
                if best_score < 20:
                    self.pee = False
                    self.countp = 0
        
        self.model.grid.move_agent(self, final_candidates[0])



    def step(self):
        self.move()
        rand = random.randint(0,10)
        randp = random.randint(0,10)
        if rand >= 2:
            self.count += 1*self.consumption
        if self.count == 100:
            #print('bar')
            self.thirst = True
        if randp >= 2:
            self.countp += 1*self.blatter
        if self.countp == 200:
            print('pee')
            self.pee = True




class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = self.max_sugar
