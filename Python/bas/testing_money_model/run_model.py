from model import MoneyModel
from model import compute_gini
import matplotlib.pyplot as plt
import numpy as np
import pandas
from mesa.batchrunner import BatchRunner
from server import server

server.port = 8521
server.launch()
# model = MoneyModel(50, 10, 10)
# for i in range(100):
#     model.step()

# gini = model.datacollector.get_model_vars_dataframe()
# gini.plot()

# plt.show()
# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# agent_wealth.head()

# plt.show()
# end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
# end_wealth.hist(bins=range(agent_wealth.Wealth.max()+1))

# # agent_counts = np.zeros((model.grid.width, model.grid.width))
# # for cell in model.grid.coord_iter():
# #     cell_content, x, y = cell
# #     agent_count = len(cell_content)
# #     agent_counts[x][y] = agent_count
# # plt.imshow(agent_counts, interpolation='nearest')
# # plt.colorbar()

# plt.show()

# fixed_params = {"width": 10,
#                 "height": 10}
# variable_params = {"N": range(10, 500, 10)}

# batch_run = BatchRunner(MoneyModel,
#                         fixed_parameters=fixed_params,
#                         variable_parameters=variable_params,
#                         iterations=5,
#                         max_steps=100,
#                         model_reporters={"Gini": compute_gini})
# batch_run.run_all()
# run_data = batch_run.get_model_vars_dataframe()
# run_data.head()
# plt.scatter(run_data.N, run_data.Gini)
# plt.show()