import numpy as np


state_list = ['BEING_AT_BAR', 'BEING_AT_WC', 'BEING_AT_STAGE', "JUST_ARRIVED",\
		  'MOVING_TO_WC', 'MOVING_TO_STAGE', 'MOVING_TO_BAR'  ]


action_list = ['DO_NOTHING','GO_TO_STAGE', 'GO_TO_BAR', 'GO_TO_WC' ]



def getNextAction(self, state):


	WAITING_TIME_AT_BAR =0
	WAITING_TIME_AT_WC = 0


	if state == 'JUST_ARRIVED':

		possible_actions = ['GO_TO_STAGE','GO_TO_WC','GO_TO_BAR']
		possible_actions_probablities = [0.9,0.05, 0.05]

		rand =random.random()
		if rand <= 0.9 :

			state = ['MOVING_TO_STAGE']
			action = 'GO_TO_STAGE'

		elif  (rand > 0.9 and rand <= (0.9 + 0.05)  ):
				
			state = 'MOVING_TO_WC'
			action = 'GO_TO_WC'

		else:

			state ='MOVING_TO_BAR'
			action = 'GO_TO_BAR'


	if state == 'BEING_AT_BAR':

		if WAITING_TIME_AT_BAR <= 5:

			WAITING_TIME_AT_BAR += 1
			action = 'DO_NOTHING'

		else:

			WAITING_TIME_AT_BAR  = 0
			state = 'MOVING_TO_STAGE'

		
	if state == 'BEING_AT_WC':

		if WAITING_TIME_AT_WC <= 5:

			WAITING_TIME_AT_WC += 1
			action = 'DO_NOTHING'

		else:

			WAITING_TIME_AT_WC = 0
			state = 'MOVING_TO_STAGE'


	if state == "MOVING_TO_STAGE":

		action = 'GO_TO_STAGE'



	if state== 'MOVING_TO_BAR':

		action = 'GO_TO_BAR'


	if state== 'MOVING_TO_WC':

		action = 'GO_TO_WC'


	if state == 'BEING_AT_STAGE':

		possible_actions = ['DO_NOTHING','GO_TO_BAR','GO_TO_WC']
		possible_actions_probablities = [0.8, 0.15, 0.05]

		rand =random.random()
		if rand <= 0.8:

			action = 'DO_NOTHING'

		elif  (rand > 0.8 and  rand <= (0.8 + 0.15) ):

			action = 'GO_TO_BAR'
			state = 'moveing_toward_Bar'

		else: 

			action ='GO_TO_WC'
			state = 'MOVING_TO_WC'

	self. state = state
	self. action = action

	return (state, action) 

