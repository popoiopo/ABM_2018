
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


import model
import agents

# variable paramter: The influence of walls (setting1)
# fixed paramters:  number of agents, grid_size, number of steps, vision for density, density coefficent, Euclidean distance coefficent

mean_utility =[]
agent_numbers = 500
number_of_steps = 1000

density_coefficent = [1,2,3,4,5]
density_vision = 3
for n in  density_coefficent:

	my_model = model.Model(agent_numbers, 50,50,0,n,density_vision)
	for t in range(number_of_steps):
		my_model.step()

	all_numOfPOIVisits =[]
	all_utility = []
	for agent in my_model.schedule.agents:
			if agent.numOfPOIVisits != 0:
				all_utility.append((agent.utility /agent.numOfPOIVisits) * 100)
				
	mean_utility.append(np.mean(all_utility))


plt.plot(vision_range,mean_utility)
plt.show()