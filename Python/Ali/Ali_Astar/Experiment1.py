
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


import model
import agents

# variable paramter: number of agents
# fixed paramters: grid_size, number of steps, density vision, and density coefficent
#  

mean_utility =[]
agent_numbers = [1,5,50,200]
number_of_steps = 500

for n in  agent_numbers:

	my_model = model.Model(n,50,50,distance_coefficent= 0.0 ,density_coefficent=0,density_vision=0)
	for t in range(number_of_steps):
		my_model.step()
		print(n,'agents','step',t)


	agent_df = my_model.datacollector.get_agent_vars_dataframe()

	all_numOfPOIVisits =[]
	all_utility = []
	for agent in my_model.schedule.agents:
			if agent.numOfPOIVisits != 0:
				all_utility.append((agent.utility /agent.numOfPOIVisits))	
	mean_utility.append(np.mean(all_utility))

plt.plot(agent_numbers,mean_utility)
plt.scatter(agent_numbers,mean_utility)
plt.xlabel('Number of Agents')
plt.ylabel('Average Utility')
plt.title('The effect of number of agents on average utility')
plt.savefig("Experiment1-DifferentNumOfAgents")
plt.grid(True)
plt.show()