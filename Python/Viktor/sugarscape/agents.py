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
<<<<<<< HEAD
    def __init__(self, pos, model, moore=True, sugar=0, metabolism=0, vision=0, closeness = 1, toilet = False, toilet_need=0.0, stepsize = 1, beer = False, beer_need = 0.0, push = 1.412):
=======
    def __init__(self, pos, model, moore=True, sugar=0, metabolism=0, vision=0, count=0, thirst=False):
>>>>>>> aec55e6856c3ce73e2a70580cade45501422acfe
        super().__init__(pos, model)
        self.pos = pos
        self.model = model
        self.moore = moore
        self.sugar = sugar
        self.toilet = toilet
        self.toilet_need = toilet_need
        self.beer = beer
        self.beer_need = beer_need
        self.metabolism = metabolism
        self.vision = vision
<<<<<<< HEAD
        self.stepsize = stepsize
        self.push = push
        
        # How close can agents stand next to eachother?
        self.closeness = closeness
=======
        self.count = count
        self.thirst = thirst
>>>>>>> aec55e6856c3ce73e2a70580cade45501422acfe

    def get_sugar(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent

    def is_occupied(self, pos, check = False):
    
        # All 1st neighbors
        if self.closeness == 1 and check == False:
            
            return len(self.model.grid.get_cell_list_contents([pos]))
        
        
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

    def BarBusy(self, bar):
        busy = 0
        (x,y) = bar
        for dx in range(4):
            for dy in range(-4,5):
                busy += len(self.model.grid.get_cell_list_contents([(abs(x-dx),y+dy)]))
        return busy
    
    
    # Find best place to go
    def score2(self, pos, center = False):
        
        (x,y) = pos
        
        if center:
            agentself = 0
        else:
            agentself = 1

        if self.toilet:
            toilet1 = get_distance(pos, (49,40))+self.push*(len(self.model.grid.get_cell_list_contents([pos]))+agentself) + self.BarBusy((49,40))
            toilet2 = get_distance(pos, (49,0))+self.push*(len(self.model.grid.get_cell_list_contents([pos]))+agentself) + self.BarBusy((49,0))
        
            score = min(toilet1, toilet2)
        
        elif self.beer:
            
            bar1 = get_distance(pos, (49,18))+self.push*(len(self.model.grid.get_cell_list_contents([pos]))+agentself) + self.BarBusy((49,18))
            bar2 = get_distance(pos, (0,18))+self.push*(len(self.model.grid.get_cell_list_contents([pos]))+agentself) + self.BarBusy((0,18))
            score = min(bar1, bar2)
            
        else:
            score = get_distance(pos, (24,49))+self.push*(len(self.model.grid.get_cell_list_contents([pos]))+agentself)

        return score


    def SearchNeighbourhoud(self, goal, current_pos):
        
        # See if Agents position, 'goal', is within reach of the position specified by current_pos
        (px,py) = current_pos
        (gx,gy) = goal
        goals = []
        pos_arounds = []
        candidates = []
        for dgx in range(-self.stepsize,self.stepsize+1):
            for dgy in range(-self.stepsize,self.stepsize+1):
                new_goal = (gx+dgx,gy+dgy)
                goals.append(new_goal)
        for dpx in range(-self.stepsize,self.stepsize+1):
            for dpy in range(-self.stepsize,self.stepsize+1):
                if px+dpx >= 0 and px+dpx < self.model.width and py+dpy >= 0 and py+dpy < self.model.height:
                    pos_around = (px+dpx,py+dpy)
                    if self.is_occupied(pos_around) == (2-self.stepsize):
                        pos_arounds.append(pos_around)
                    if pos_around == goal:
                        return current_pos
        for pos in pos_arounds:
            if pos in goals:
                candidates.append(pos)
        
        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) == 0:
            return False
        else:
            min_dist = min([get_distance(current_pos, pos) for pos in candidates])
            final_candidates = [pos for pos in candidates if get_distance(current_pos, pos) == min_dist]
            return final_candidates[0]
                
        return False
        
    def MoveInNeigbourhood(self, current_pos, alreadySearched):
        
        # Search one stepsize around current_pos.
        possible_moves = []
        (x,y) = current_pos
        for dx in range(-self.stepsize, self.stepsize+1):
            for dy in range(-self.stepsize,self.stepsize+1):
                if dx == self.stepsize or dy == self.stepsize:
                    if x+dx >= 0 and x+dx < self.model.width and y+dy >= 0 and y+dy < self.model.height:
                        pos_next = (x+dx, y+dy)
                        if not pos_next in alreadySearched:
                            alreadySearched.append(pos_next)
                            if self.is_occupied(pos_next) == 0:
                                possible_moves.append(pos_next)
        return possible_moves, alreadySearched



    def LocalAstar(self, candidates, own_pos):
        
        # The local Astar algorithm is calculating backward
        # from the position with the highest score, sorted in candidates
        # It starts in a candidates gridpoint and steps untill it finds the agent position in 'own_pos'
        # Stepsize: How many grippoints can the agents walk in 1 step
        if self.is_occupied(own_pos, True) > 1:
            self.stepsize = 1
        else:
            self.stepsize = 2
        
        
        possible_moves1 = []
        for pos in candidates:
            alreadySearched = []
            # First search within stepsize
            if own_pos == pos:
                print('v0')
                return pos
            elif self.SearchNeighbourhoud(own_pos,pos) != False:
                print('v1')
                return self.SearchNeighbourhoud(self.pos, pos)
        
            else:
                possible_moves, alreadySearched = self.MoveInNeigbourhood(pos, alreadySearched)
                for temppos in possible_moves:
                    possible_moves1.append(temppos)
                
            possible_moves2 = []
            if len(possible_moves1) > 0:
                
                # Second search within stepsize of first step.
                for pos1 in possible_moves1:
                    if not self.SearchNeighbourhoud(own_pos, pos1) == False:
                        print('v2')
                        return self.SearchNeighbourhoud(own_pos,pos1)
        
                for pos1 in possible_moves1:
                    possible_moves, alreadySearched2 = self.MoveInNeigbourhood(pos1, alreadySearched)
                    for temppos in possible_moves:
                        possible_moves2.append(temppos)

                possible_moves3 = []
                if len(possible_moves2) > 0:
                    
                    # Third search within stepsize of second step.
                    for pos2 in possible_moves2:
                        if not self.SearchNeighbourhoud(own_pos, pos2) == False:
                            print('v3')
                            return self.SearchNeighbourhoud(own_pos, pos2)
                                
                    for pos2 in possible_moves2:
                        possible_moves, alreadySearched3 = self.MoveInNeigbourhood(pos2, alreadySearched2)
                        for temppos in possible_moves:
                            possible_moves3.append(temppos)
                            
                    possible_moves4 = []
                    if len(possible_moves3) > 0:
                        for pos3 in possible_moves3:
                            if not self.SearchNeighbourhoud(own_pos, pos3) == False:
                                print('v4')
                                return self.SearchNeighbourhoud(own_pos, pos3)
                        
                        for pos3 in possible_moves3:
                            possible_moves, alreadySearched4 = self.MoveInNeigbourhood(pos3, alreadySearched3)
                            for temppos in possible_moves:
                                possible_moves4.append(temppos)
                                
                        if len(possible_moves4) >0:
                            for pos4 in possible_moves4:
                                if not self.SearchNeighbourhoud(own_pos, pos4) == False:
                                    print('v5')
                                    return self.SearchNeighbourhoud(own_pos, pos4)
        
        print('out') # If unable to move, stand still for this step.
        return own_pos


    def GetNeighbors(self, pos, vision):
        # Get neighborhood within vision
        (x,y) = pos
        neighbors = []
        if self.is_occupied(pos, True) > 1:
            self.vision = 2
        else:
            self.vision = 5
        
        for dx in range(-vision,vision+1):
            for dy in range(-vision,vision+1):
                if x+dx >= 0 and x+dx < self.model.width and y+dy >= 0 and y+dy < self.model.height:
                    pos = (x+dx,y+dy)
                    if abs(dx) > 1 or abs(dy) > 1:
                        if self.is_occupied(pos) == 0:
                            neighbors.append(pos)
                    else:
                        if self.is_occupied(pos) == 1:
                            neighbors.append(pos)
        
        neighbors.append(self.pos)
        return neighbors
            

    def move2(self):

        (x,y) = self.pos
        
        self.toilet_need += 0.0002*np.random.random()
        if np.random.random() < self.toilet_need:
            self.toilet = True
       
        if x > 48 and y == 40:
            self.toilet_need -= 0.01
            if self.toilet_need < 0:
                self.toilet = False
    
        if x > 45 and y < 5:
            self.toilet_need -= 0.02
            if self.toilet_need < 0:
                self.toilet = False
    
        self.beer_need += 0.002*np.random.random()
        if np.random.random() < self.beer_need:
            self.beer = True
        
        if x > 48 and 15 < y < 20:
            self.beer_need -= 0.02
            if self.beer_need < 0:
                self.beer = False
    
        if x < 1 and 15 < y < 20:
            self.beer_need -= 0.05
            if self.beer_need < 0:
                self.beer = False
        
    
        if self.is_occupied(self.pos, True) > 7:
            self.vision = 1
        else:
            self.vision = 2


        scores = []
        around = []
        
        for dx in range(-self.vision, self.vision+1):
            for dy in range(-self.vision, self.vision+1):
                if x+dx >= 0 and x+dx < self.model.width and y+dy >= 0 and y+dy < self.model.height:
                    pos = (x+dx, y+dy)
                    around.append(pos)
                    if dx == 0 and dy == 0:
                        scores.append(self.score2(pos, center=True))
                    else:
                        scores.append(self.score2(pos))

        best_pos = around[np.argmin(scores)]
        self.model.grid.move_agent(self, best_pos)

    def move(self):
        
        
        self.toilet_need += 0.0002#*np.random.random()
        if np.random.random() < self.toilet_need:
            self.toilet = True
    
        (x,y) = self.pos
        
        if x > 94 and 46 < y < 53:
            self.toilet = False
            self.toilet_need = 0.0

        def second_smallest(numbers):
            return nsmallest(2, numbers)[-1]
        
        #def third_smallest(numbers):
        #    return nsmallest(3, numbers)[-2]
        
        neighbors = self.GetNeighbors(self.pos, self.vision)

        
        
        # Choose best place
        if len(neighbors) == 1:
            final_candidates = neighbors
        else:
            
            best_score =  min([self.score(pos) for pos in neighbors])
            candidates = [pos for pos in neighbors if self.score(pos)== best_score]
            #second_best_score = second_smallest([self.score(pos) for pos in neighbors])
            #second_candidates = [pos for pos in neighbors if self.score(pos) == second_best_score]
            #third_best_score = third_smallest([self.score(pos) for pos in neighbors])
            #third_candidates = [pos for pos in neighbors if self.score(pos) == third_best_score]
            min_dist = min([get_distance(self.pos, pos) for pos in candidates])
            final_candidates = [pos for pos in candidates if get_distance(self.pos,pos) == min_dist]
            temp = [pos for pos in candidates if get_distance(self.pos,pos) != min_dist]
            for tup in temp:
                final_candidates.append(tup)
                #for tup2 in second_candidates:
                #final_candidates.append(tup2)
                #for tup3 in third_candidates:
                #final_candidates.append(tup3)
        
        
        #(xx,yy) = self.LocalAstar(final_candidates, (x,y))
        #self.model.grid.move_agent(self, (xx,yy))
        self.model.grid.move_agent(self, final_candidates[0])
 
    def step(self):
<<<<<<< HEAD
        self.move2()
=======
        self.move()
        rand = random.randint(0,10)
        if rand >= 2:
            self.count += 1
        if self.count == 30:
            print('bar')
            self.thirst = True



>>>>>>> aec55e6856c3ce73e2a70580cade45501422acfe

class Sugar(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.amount = len(self.model.grid.get_cell_list_contents([pos]))
    
    
    def step(self):
        self.amount = len(self.model.grid.get_cell_list_contents([self.pos]))
        if self.amount > 2:
            print('############################')
            print(self.amount)

