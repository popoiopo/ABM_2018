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
    def __init__(self, pos, model, moore=True, sugar=0, metabolism=0, vision=0, count=0, thirst=False, pee=False, countp=0):
        super().__init__(pos, model)
        self.pos = pos

        
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        self.count = count
        self.thirst = thirst
        self.pee = pee
        self.countp = countp

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
            pos2 = (x,y)
        elif x == 49:
            pos1 = (x,y)
        if y == 0:
            pos4 = (x,y)
        elif y == 49:
            pos3 = (x,y)
    
        this_cell = self.model.grid.get_cell_list_contents([pos,pos1, pos2, pos3, pos4])
        return len(this_cell) > 1


    def move(self):
        # Get neighborhood within vision
        (x,y) = self.pos
        neighbors = []
        for dx in range(-1,2):
            for dy in range(-1,2):
                if x+dx >= 0 and x+dx < 50 and y+dy >= 0 and y+dy < 50:
                    pos = (x+dx,y+dy)
                    if not self.is_occupied(pos):
                        neighbors.append(pos)
        neighbors.append(self.pos)
        # Find best place to go
        def score(pos):
            x,y = pos
            score = 1.5 * y + 24.5 - abs(x - 24.5)
            score_bar = 1.5 * x + 24.5 - abs(y - 24.5) 
            score_p = 1.5 * x + 24.5 + abs(y - 24.5)
            return score, score_bar, score_p
        
        if self.pee == True:   
            best_score =  max([score(pos)[2] for pos in neighbors])
            candidate = [pos for pos in neighbors if score(pos)[2]==
                    best_score]
            if best_score > 80:
                print('piss', best_score)
                self.pee = False
                print(self.thirst) 
                self.countpp = 0
                print(self.count)

        elif self.thirst == True:   
            best_score =  max([score(pos)[1] for pos in neighbors])
            candidate = [pos for pos in neighbors if score(pos)[1]==
                    best_score]
            if best_score > 80:
                print('thirsty', best_score)
                self.thirst = False
                print(self.thirst) 
                self.count = 0
                print(self.count)
        else:    
            best_score =  max([score(pos)[0] for pos in neighbors])
            candidate = [pos for pos in neighbors if score(pos)[0]==
                    best_score]
            

        self.model.grid.move_agent(self, candidate[0])
    
    
    
    def move2(self):
        # Get neighborhood within vision
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, False,
                False, radius=self.vision) if not self.is_occupied(i)]
        neighbors.append(self.pos)
        # Look for location with the most sugar
        if self.thirst == False:
            max_sugar = max([self.get_sugar(pos).amount for pos in neighbors])
            candidates = [pos for pos in neighbors if self.get_sugar(pos).amount ==
                    max_sugar]
        if self.thirst == True:
            max_sugar = min([self.get_sugar(pos).amount for pos in neighbors])
            candidates = [pos for pos in neighbors if self.get_sugar(pos).amount ==
                    max_sugar]
        """
        # Narrow down to the nearest ones
        min_dist = min([get_distance(self.pos, pos) for pos in candidates])
        final_candidates = [pos for pos in candidates if get_distance(self.pos,
            pos) == min_dist]
        """
        random.shuffle(candidates)
        
        self.model.grid.move_agent(self, candidates[0])
        print(candidates[0], "kaaaaaaaaaaaaaaaaaaaaan")
        if candidates[0] >=60:
            self.thirsty == False

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
        
        rand = random.randint(0, 10)
        randp = random.randint(0, 10)
        #print(rand)
        if rand > 8:
            self.count += 1
        if randp > 8:
            self.count += 1
        #print(self.count, "count")
        if self.count == 40:
            print('bar')
            #self.model.grid._remove_agent(self.pos, self)
            #self.model.schedule.remove(self)
            self.thirst = True
        if self.countp == 30:
            self.pee = True


class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = self.max_sugar


