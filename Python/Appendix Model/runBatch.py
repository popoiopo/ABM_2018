import matplotlib.pyplot as plt

from ClubLife.model import *
from ClubLife.agents import *

import timeit

start = timeit.default_timer()

my_model = Model(60, 50, 50)
for t in range(200):
    my_model.step()
    print(t)

# model_df = my_model.dc.get_model_vars_dataframe()
agent_df = my_model.datacollector.get_agent_vars_dataframe()
# print(agent_df.to_string())

all_numOfPOIVisits = []
all_utility = []
for agent in my_model.schedule.agents:
    if agent.numOfPOIVisits != 0:
      all_numOfPOIVisits.append([agent.numOfPOIVisits, (agent.utility / agent.numOfPOIVisits) * 100])
      all_utility.append((agent.utility / agent.numOfPOIVisits) * 100)

# for i in  all_numOfPOIVisits:
#   plt.scatter(i[0],i[1] )

plt.hist(all_utility)

stop = timeit.default_timer()
print(stop - start)

# plt.plot(all_numOfPOIVisits)

# agent_df['numOfPOIVisits'].plot()
plt.show()
