# run.py
import numpy as np
import sys
import matplotlib.pyplot as plt

from server import server


# sys.path.append('')



#model = MoneyModel(50, 10, 10)
#for i in range(100):
#    model.step()

#agent_counts = np.zeros((model.grid.width, model.grid.height))
#for cell in model.grid.coord_iter():
#    cell_content, x, y = cell
#    agent_count = len(cell_content)
#    agent_counts[x][y] = agent_count
#plt.imshow(agent_counts, interpolation='nearest')
#plt.colorbar()
# If running from a text editor or IDE, remember you'll need the following:
#plt.show()

#agent_wealth = [a.wealth for a in model.schedule.agents]
#plt.hist(agent_wealth)
#plt.show()

#gini = model.datacollector.get_model_vars_dataframe()
#gini.plot()


server.port = 8528 # The default
server.launch()