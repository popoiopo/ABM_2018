from mesa_own.visualization.modules import CanvasGrid
from mesa_own.visualization.ModularVisualization import ModularServer
from mesa_own.visualization.UserParam import UserSettableParameter

from ClubLife_no_walls.model import *
from ClubLife_no_walls.agents import *
import randomcolor
from colour import Color


def agent_portrayal(agent):

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 1,
                 "Layer": 0,
                 "Color": "white"}

    if type(agent) is commuterAgent and agent.layer is "BAR":
        portrayal["Color"] = "green"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.5

    if type(agent) is commuterAgent and agent.layer is "STAGE":
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5

    if type(agent) is commuterAgent and agent.layer is "BAR2":
        portrayal["Color"] = "red"
        portrayal["Layer"] = 4
        portrayal["r"] = 0.5

    if type(agent) is nodeAgent and agent.block is True:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5

    if type(agent) is nodeAgent and agent.POI is True and agent.block is False:
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 1
        portrayal["r"] = 1

    return portrayal


n_slider = UserSettableParameter("slider", "Number of agents", 200, 1, 1500, 1)
chart = ChartModule(250, 500)
chart_util = ChartModuleUtil(250, 500)
histogram = HistogramModule(list(range(10)), 250, 500)
grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
domain_size = 50
server = ModularServer(Model,
                       [grid, histogram, chart, chart_util],
                       "ABM Project",
                       {"N": n_slider, "width": domain_size, "height": domain_size})
