
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


import model
import agents

# variable paramter: vision_range, and coefficent 2
# fixed paramters:  number of agents, grid_size, number of steps, density vision, and density coefficent

mean_utility =[]
agent_numbers = 200
number_of_steps = 600

vision_range = [2,4,5]
for n in  vision_range:
	my_model = model.Model(agent_numbers, 50,50,distance_coefficent= 0 ,density_coefficent=5,density_vision= n)
	for t in range(number_of_steps):
		my_model.step()
		print(n,t)
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
plt.title('The effect of vision on average utility')
plt.savefig("Experiment2-DifferentVisions-d1-n200")
plt.grid(True)

plt.show()