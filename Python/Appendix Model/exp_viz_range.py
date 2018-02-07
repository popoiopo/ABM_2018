import matplotlib.pyplot as plt
import numpy as np

from ClubLife.model import *
from ClubLife.agents import *

# variable paramter: vision_range, and coefficent 2
# fixed paramters:  number of agents, grid_size, number of steps, density vision, and density coefficent

mean_utility = []
agent_numbers = 200
number_of_steps = 1800

vision_range = [2, 3, 4, 5, 6]
for n in vision_range:
    my_model = Model(agent_numbers, 50, 50, distance_coefficent=0, density_coefficent=5, density_vision=n)
    for t in range(number_of_steps):
        my_model.step()
        print(n, t)
    all_numOfPOIVisits = []
    all_utility = []
    for agent in my_model.schedule.agents:
        if agent.numOfPOIVisits != 0:
            all_utility.append((agent.utility / agent.numOfPOIVisits) * 100)

    mean_utility.append(np.mean(all_utility))


plt.plot(vision_range, mean_utility)
plt.scatter(vision_range, mean_utility)
plt.xlabel('Vision Range')
plt.ylabel('Average Utility')
plt.title('The effect of vision on average utility')
plt.savefig("figures/DifferentVisions-d1-n200")
plt.grid(True)

plt.show()
