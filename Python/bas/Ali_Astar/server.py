from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from model import Model
import model
import agents
import randomcolor

def agent_portrayal(agent):




    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 1}

    if type(agent) is agents.nodeAgent:
        portrayal["Color"] = "white"
        portrayal["Layer"] = 0


    if type(agent) is agents.nodeAgent and agent.block==True:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0

    if type(agent) is agents.commuterAgent:

        portrayal["Color"] = randomcolor.RandomColor(agent.unique_id + 1).generate()
        portrayal["Layer"] = 2

    if type(agent) is agents.POIAgent:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1







    # if agent.wealth > 0:
    #     portrayal["Color"] = "red"
    #     portrayal["Layer"] = 0

    return portrayal

n_slider = UserSettableParameter("slider", "Numer of agents", 100, 2, 200, 1)
grid = CanvasGrid(agent_portrayal, 50, 50, 600, 600)

server = ModularServer(Model,
                       [grid],
                       "ABM Project",
                       {"N": n_slider, "width": 50, "height": 50})


