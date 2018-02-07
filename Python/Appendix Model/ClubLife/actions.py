import random
import math


def get_distance(pos_1, pos_2):

    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx ** 2 + dy ** 2)


def getNextAction(self, state, POI_dict):

    state = self.state
    layer = self.layer

    x = self.pos[0]
    y = self.pos[1]

##################### JUST ARRIVED rules ###############################

    if state == 'JUST_ARRIVED':

        actions = ['GO_TO_STAGE', 'GO_TO_BAR2', 'GO_TO_BAR']

        # Testing
        actions = ['GO_TO_STAGE', 'GO_TO_BAR']

        actions_probablities = [0.99, 0.005, 0.005]

        rand = random.uniform(0, 1)
        if rand <= actions_probablities[0]:

            state = 'MOVING_TO_STAGE'

            layer = "STAGE"
            self.move('STAGE')

        # elif (rand > actions_probablities[0] and rand <=
        #       (actions_probablities[0] + actions_probablities[1])):

        #   state = 'MOVING_TO_BAR2'

        #   self.shortest_time = self.model.POI_cost['BAR2'][x][y] -1

        #   layer = "BAR2"
        #   self.total_waiting = 0

        #   self.move('BAR2')

        else:

            state = 'MOVING_TO_BAR'

            self.shortest_time = self.model.POI_cost['BAR'][x][y] - 1

            layer = "BAR"
            self.total_waiting = 0

            self.move('BAR')



##################### STAGE Rules ###############################

    elif state == "MOVING_TO_STAGE":

        layer = "STAGE"
        self.move('STAGE')

        # TO DO: inner states at stage, try to get closer, if they see empty spaces
        # TO DO: placing the agents when they arrive at stage
        if get_distance(self.pos, POI_dict['STAGE']) <= 20:

            state = "BEING_AT_STAGE"

    elif state == 'BEING_AT_STAGE':

        pos_act = ['GO_TO_STAGE', 'GO_TO_BAR']
        # , 'GO_TO_BAR2']
        pos_act_prob = [0.005, 0.005, 0.99]

        rand = random.random()

        if rand <= pos_act_prob[0]:

            self.shortest_time = self.model.POI_cost['BAR'][x][y] - 1

            # print("shortest_time",self.shortest_time)
            state = 'MOVING_TO_BAR'
            layer = 'BAR'
            self.total_waiting +=1
            self.move('BAR')

        # elif (rand > pos_act_prob[0] and rand <= (pos_act_prob[0] + pos_act_prob[1])):

        #   self.shortest_time = self.model.POI_cost['BAR2'][x][y] -1
        #   # print("shortest_time",self.shortest_time)
        #   state = 'MOVING_TO_BAR2'
        #   layer = 'BAR2'
        #   self.total_waiting +=1
        #   self.move('BAR2')

        else:

            layer = 'STAGE'
            self.move('STAGE')


###################### BAR1 rules ##############################

    elif state == 'MOVING_TO_BAR':

        if get_distance(self.pos,POI_dict['BAR']) <= 2:

            state = "BEING_AT_BAR"
            self.total_waiting += 1
            self.WAITING_TIME_AT_POI += 1

        else:
            self.total_waiting += 1
            self.move('BAR')
            layer = "BAR"

    elif state == 'BEING_AT_BAR':

        if self.WAITING_TIME_AT_POI < self.model.serving_time['BAR']:

            self.total_waiting += 1
            self.WAITING_TIME_AT_POI += 1

            layer = "BAR"

        else:

            self.utility +=\
             (self.shortest_time + self.model.serving_time['BAR']) / (self.total_waiting)
            self.numOfPOIVisits += 1
            self.util = self.utility / self.numOfPOIVisits
            # print(self.numOfPOIVisits)
            # print(self.utility)
            # print(self.shortest_time)
            # print(self.model.serving_time['BAR'])
            # print(self.total_waiting - self.shortest_time - self.model.serving_time['BAR'])
            self.WaitingTime = self.total_waiting
            self.total_waiting = 0
            self.WAITING_TIME_AT_POI = 0

            state = 'MOVING_TO_STAGE'
            layer = "STAGE"

            self.move('STAGE')


####################### BAR2 rules #############################

    # elif state == 'MOVING_TO_BAR2':

    #   if get_distance(self.pos, POI_dict['BAR2']) <= 2:

    #       state = "BEING_AT_BAR2"
    #       self.total_waiting +=1
    #       self.WAITING_TIME_AT_POI +=1

    #       ####change toal_waiting, to total cost

    #   else:
    #       self.total_waiting +=1
    #       self.move('BAR2')
    #       layer = 'BAR2'

    # elif state == 'BEING_AT_BAR2':

    #   if self.WAITING_TIME_AT_POI < self.model.serving_time['BAR2']:

    #       self.total_waiting += 1
    #       self.WAITING_TIME_AT_POI += 1
    #       layer = "BAR2"

    #   else:

    #       self.utility +=\
    #        (self.shortest_time + self.model.serving_time['BAR2']) / (self.total_waiting)
    #       self.numOfPOIVisits += 1
    #       self.util = self.utility / self.numOfPOIVisits
    #       print(self.utility)

    #       # print(self.numOfPOIVisits)
    #       # print(self.utility)
    #       # print(self.shortest_time)
    #       # print(self.model.serving_time['BAR'])
    #       # print(self.total_waiting - self.shortest_time)
    #       self.WaitingTime = self.total_waiting
    #       self.total_waiting =0
    #       self.WAITING_TIME_AT_POI = 0

    #       state = 'MOVING_TO_STAGE'
    #       layer = "STAGE"
    #       self.move('STAGE')

    # print(self.total_waiting)
    # print(state)
    self. state = state
    self. layer = layer
    return (state)
