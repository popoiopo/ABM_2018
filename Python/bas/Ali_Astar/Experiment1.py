
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


import model
import agents

# variable paramter: number of agents
# fixed paramters: grid_size, number of steps, density vision, and density coefficent

mean_utility =[]
agent_numbers = [2,10,100,1000]
number_of_steps = 1000

for n in  agent_numbers:

	my_model = model.Model(n, 50,50)
	for t in range(number_of_steps):
		my_model.step()
		#print(t)


	agent_df = my_model.datacollector.get_agent_vars_dataframe()

	all_numOfPOIVisits =[]
	all_utility = []
	for agent in my_model.schedule.agents:
			if agent.numOfPOIVisits != 0:
				all_utility.append((agent.utility /agent.numOfPOIVisits) * 100)
				
	mean_utility.append(np.mean(all_utility))


plt.plot(agent_numbers,mean_utility)
plt.show()