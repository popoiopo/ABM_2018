
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


import model
import agents

# variable paramter: density_coefficent
# fixed paramters:  number of agents, grid_size, number of steps, vision for density

mean_utility =[]
agent_numbers = 500
number_of_steps = 1000

density_coefficent = [1,2,3,4,5]
density_vision = 3
for n in  density_coefficent:

	my_model = model.Model(agent_numbers, 50,50,0,n,density_vision)
	
	for t in range(number_of_steps):
		print(n,t)
		my_model.step()

	all_numOfPOIVisits =[]
	all_utility = []
	for agent in my_model.schedule.agents:
			if agent.numOfPOIVisits != 0:
				all_utility.append((agent.utility /agent.numOfPOIVisits) * 100)
				
	mean_utility.append(np.mean(all_utility))



plt.plot(vision_range,mean_utility)
plt.scatter(vision_range,mean_utility)
plt.xlabel('Vision Range')
plt.ylabel('Average Utility')
plt.title('The effect of density coefficent on average utility')
plt.savefig("Experiment3-DifferentDensityCoefficent")
plt.grid(True)

plt.show()