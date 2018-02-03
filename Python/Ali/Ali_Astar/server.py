from mesa_own.visualization.modules import CanvasGrid
from mesa_own.visualization.ModularVisualization import ModularServer
from mesa_own.visualization.UserParam import UserSettableParameter


import model
import agents
import randomcolor
from colour import Color

def agent_portrayal(agent):

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 1,
                 "Layer": 0,
                 "Color":"white"}

    # if type(agent) is agents.nodeAgent and agent.block is False:

    #     max_star = 300

    #     # Average Coloring
    #     test = agent.locations["STAGE"] + agent.locations["BAR"] + agent.locations["WC"]
    #     portrayal["Color"] = Color(hue=(test / max_star) * -1 + 1, saturation=(test / max_star) * -1 + 1, luminance=(test / max_star) * -1 + 1).hex


    #     # Coloring single area (stage)
    #     # portrayal["Color"] = Color(hue=(agent.locations["STAGE"] / max_star) * -1 + 1, saturation=(agent.locations["STAGE"] / max_star) * -1 + 1, luminance=(agent.locations["STAGE"] / max_star) * -1 + 1).hex
    #     # portrayal["Color"] = Color(hue=(30) * -1 + 1, saturation=(agent.locations["STAGE"] / max_star) * -1 + 1, luminance=(agent.locations["STAGE"] / max_star) * -1 + 1).hex


    if type(agent) is agents.commuterAgent and agent.layer is "BAR":
        portrayal["Color"] = "green"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.5

    if type(agent) is agents.commuterAgent and agent.layer is "STAGE":
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5

    if type(agent) is agents.commuterAgent and agent.layer is "BAR2":
        portrayal["Color"] = "red"
        portrayal["Layer"] = 4
        portrayal["r"] = 0.5

    if type(agent) is agents.nodeAgent and agent.block  is True:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5

    if type(agent) is agents.nodeAgent and agent.POI is True and  agent.block is  False:
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 1
        portrayal["r"] = 1

    return portrayal

n_slider = UserSettableParameter("slider", "Number of agents", 200, 1, 1500, 1)
#domain_size = UserSettableParameter("slider", "GridSize", 50, 50, 50, 1)
grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
domain_size = 50
server = ModularServer(model.Model,
                       [grid],
                       "ABM Project",
                       {"N": n_slider, "width": domain_size, "height": domain_size })
