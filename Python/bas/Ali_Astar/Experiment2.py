
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


import model
import agents

# variable paramter: vision_range, and coefficent 2
# fixed paramters:  number of agents, grid_size, number of steps, density vision, and density coefficent

mean_utility =[]
agent_numbers = 400
number_of_steps = 400

vision_range = [2,4]
for n in  vision_range:
	print(n)
	my_model = model.Model(agent_numbers, 50,50,0,2,n)
	for t in range(number_of_steps):
		my_model.step()
		print(t)
	all_numOfPOIVisits =[]
	all_utility = []
	for agent in my_model.schedule.agents:
			if agent.numOfPOIVisits != 0:
				all_utility.append((agent.utility /agent.numOfPOIVisits) * 100)
				
	mean_utility.append(np.mean(all_utility))


plt.plot(vision_range,mean_utility)
plt.show()