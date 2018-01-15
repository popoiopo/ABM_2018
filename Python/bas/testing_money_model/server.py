from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import MoneyModel
from model import HistogramModule
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import VisualizationElement
import numpy as np

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled" : "true",
                 "r": 0.5}
    if agent.wealth > 0:
      portrayal["Color"] = "red"
      portrayal["Layer"] = 0
    else:
      portrayal["Color"] = "steelblue"
      portrayal["Layer"] = 1
      portrayal["r"] = 0.2
    return portrayal

n_slider = UserSettableParameter("slider", "Numer of agents", 100, 2, 200, 1)
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                      data_collector_name='datacollector')
# server = ModularServer(MoneyModel,
#                        [grid, chart],
#                        "Money Model",
#                        {"N": n_slider, "width": 10, "height": 10})

histogram = HistogramModule(list(range(10)), 200, 500)
server = ModularServer(MoneyModel,
   [grid, chart, histogram],
   "Money Model",
   {"N": n_slider, "width": 10, "height": 10})