import random
import math
import numpy as np
from mesa import Agent
from heapq import nsmallest


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
    def __init__(self, pos, model, beta_c, beta_d, beta_w, beer_consumption, serving_speed, moore=True, vision=2, beer = False):

        super().__init__(pos, model)
        self.pos = pos
        self.model = model
        self.moore = moore
        self.beer = beer
        self.beer_consumption = np.random.normal(beer_consumption, 0.0001)
        self.serving_speed = serving_speed
        self.beer_need = np.random.random()
        self.vision = vision
        self.beta_c = beta_c        # Crowd
        self.beta_d = beta_d        # Distance
        self.beta_w = beta_w        # Waiting time
        self.waiting = 0
        self.helped = 0
        self.Que = 0
        self.InQue = False
    


    def get_sugar(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent

    def is_occupied(self, pos, check = False):
    
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


    
    
    # Find best place to go
    def score2(self, pos, center = False):
        
        if center:
            agentself = 1
        else:
            agentself = 0
        
        (x,y) = pos
        crowd = (len(self.model.grid.get_cell_list_contents([pos]))-agentself)

        if self.beer:
            
            adjusted_beta_c = max(self.beta_c - self.waiting*0.05, 1.3)
            score_bar1 = self.beta_d*get_distance(pos, self.model.bar1) + adjusted_beta_c*crowd + self.beta_w*self.model.bar1crowd
            score_bar2 = self.beta_d*get_distance(pos, self.model.bar2) + adjusted_beta_c*crowd + self.beta_w*self.model.bar2crowd
            score_bar3 = self.beta_d*get_distance(pos, self.model.bar3) + adjusted_beta_c*crowd + self.beta_w*self.model.bar3crowd
            score_bar4 = self.beta_d*get_distance(pos, self.model.bar4) + adjusted_beta_c*crowd + self.beta_w*self.model.bar4crowd

            score = min(score_bar1, score_bar2, score_bar3, score_bar4)
            
        else:
            score = self.beta_d*get_distance(pos, self.model.stage)+self.beta_c*crowd

        return score



    def move2(self):

        (x,y) = self.pos
        
        abc = False
        
        (b1x, b1y) = self.model.bar1
        (b2x, b2y) = self.model.bar2
        (b3x, b3y) = self.model.bar3
        (b4x, b4y) = self.model.bar4
        
        # If bars on same spot Serving Speed doubles.
        if b1y == b3y:
            S = 2
        else:
            S = 1
        
        self.beer_need += self.beer_consumption*2*np.random.random()
            
        if 1.0 < self.beer_need:
            self.beer = True
        

        
        if self.beer == True and abs(x-b1x)*abs(x-b2x)*abs(x-b3x)*abs(x-b4x) < 10 and abs(y-b1y)*abs(y-b2y)*abs(y-b3y)*abs(y-b4y) < 10:
            self.helped += S*self.serving_speed/(len(self.model.grid.get_cell_list_contents([self.pos]))-1)
            if self.helped >= 1.0:
                self.beer_need = 0.0
                self.beer = False
                self.InQue = True
                self.waiting = 0
                self.helped = 0
       
    
    
        if self.is_occupied(self.pos, True) > 7:
            self.vision = 1
        else:
            self.vision = 2
        
        
        if self.beer == True:
            self.waiting += 1
        
        if self.InQue == True:
            self.Que += 1
    
        if self.Que > 6:
            self.InQue =  False
            self.Que = 0
        
        if self.waiting != 0:
            self.model.WaitingTimes.append(self.waiting)
        
        
        
        
        scores = []
        around = []
        
        for dx in range(-self.vision, self.vision+1):
            for dy in range(-self.vision, self.vision+1):
                if 0 <= (x+dx) < self.model.width and 0 <= (y+dy) < self.model.height:
                    pos = (x+dx, y+dy)
                    if self.Que > 0 or len(self.model.grid.get_cell_list_contents([pos])) < 3 or (self.beer ==  True and len(self.model.grid.get_cell_list_contents([pos])) < 5):
                        around.append(pos)
                        if (self.beer and self.helped == 0) or self.InQue:
                            scores.append(self.score2(pos, center=False))
                        elif dx == 0 and dy == 0:
                            scores.append(self.score2(pos, center=True))
                        else:
                            scores.append(self.score2(pos, center=False))


        if len(scores) < 1:
            self.model.grid.move_agent(self, self.pos)
        
        else:
            best_pos = around[np.argmin(scores)]
            self.model.grid.move_agent(self, best_pos)

    
    def step(self):
        self.move2()



class Sugar(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.counter = 0
        self.amount = len(self.model.grid.get_cell_list_contents([self.pos]))
        
    
    def step(self):
        self.counter += 1
        self.amount = len(self.model.grid.get_cell_list_contents([self.pos]))
        if self.counter > 270 and self.amount > self.model.MaxAgents:
            self.model.MaxAgents =  self.amount



