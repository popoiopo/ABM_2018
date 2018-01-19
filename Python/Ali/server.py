from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Model
import model
import agents

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

        portrayal["Color"] = "red" 
        portrayal["Layer"] = 2
    
    if type(agent) is agents.POIAgent:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    






    # if agent.wealth > 0:
    #     portrayal["Color"] = "red"
    #     portrayal["Layer"] = 0
   
    return portrayal

grid = CanvasGrid(agent_portrayal, 50, 50, 600, 600)

server = ModularServer(Model,
                       [grid],
                       "ABM Project",
                       {"N": 100, "width": 50, "height": 50})


