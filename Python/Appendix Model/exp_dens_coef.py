import matplotlib.pyplot as plt
import numpy as np

from ClubLife.model import *
from ClubLife.agents import *

# variable paramter: density_coefficent
# fixed paramters:  number of agents, grid_size, number of steps, vision for density

mean_utility1 = []
mean_utility2 = []
mean_utility3 = []
agent_numbers = 200
number_of_steps = 1800

density_coefficent = [1, 2, 3, 4, 5]
# density_coefficent = [5, 20, 50, 100, 150]
density_vision = 3
for n in density_coefficent:

    my_model1 = Model(agent_numbers, 50, 50, 0, n, density_vision)
    my_model2 = Model(agent_numbers, 50, 50, 0, n, density_vision)
    my_model3 = Model(agent_numbers, 50, 50, 0, n, density_vision)

    for t in range(number_of_steps):
        print(n, t)
        my_model1.step()

    all_numOfPOIVisits1 = []
    all_utility1 = []
    for agent in my_model1.schedule.agents:
        if agent.numOfPOIVisits != 0:
            all_utility1.append((agent.utility / agent.numOfPOIVisits) * 100)

    mean_utility1.append(np.mean(all_utility1))

    for t in range(number_of_steps):
        print(n, t)
        my_model2.step()

    all_numOfPOIVisits2 = []
    all_utility2 = []
    for agent in my_model2.schedule.agents:
        if agent.numOfPOIVisits != 0:
            all_utility2.append((agent.utility / agent.numOfPOIVisits) * 100)

    mean_utility2.append(np.mean(all_utility2))

    for t in range(number_of_steps):
        print(n, t)
        my_model3.step()

    all_numOfPOIVisits3 = []
    all_utility3 = []
    for agent in my_model3.schedule.agents:
        if agent.numOfPOIVisits != 0:
            all_utility3.append((agent.utility / agent.numOfPOIVisits) * 100)

    mean_utility3.append(np.mean(all_utility3))


plt.plot(density_coefficent, mean_utility1, 'r--', density_coefficent, mean_utility2, 'b--', density_coefficent, mean_utility3, 'g--')
# plt.scatter(density_coefficent, mean_utility)
plt.xlabel('Density Range')
plt.ylabel('Average Utility')
plt.title('The effect of stochasticity with variation of density on average utility')
plt.savefig("figures/DifferentDensityCoefficent_stoch")
plt.grid(True)

plt.show()
