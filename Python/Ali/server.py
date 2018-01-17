from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import MoneyModel
import model

def agent_portrayal(agent):




    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 1}

    if type(agent) is model.nodeAgent:
        portrayal["Color"] = "white"
        portrayal["Layer"] = 0

    if type(agent) is model.MoneyAgent:

        portrayal["Color"] = "red" 
        portrayal["Layer"] = 2
    
    if type(agent) is model.POIAgent:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    






    # if agent.wealth > 0:
    #     portrayal["Color"] = "red"
    #     portrayal["Layer"] = 0
   
    return portrayal

grid = CanvasGrid(agent_portrayal, 100, 100, 800, 800)

server = ModularServer(MoneyModel,
                       [grid],
                       "ABM Project",
                       {"N": 10, "width": 100, "height": 100})


