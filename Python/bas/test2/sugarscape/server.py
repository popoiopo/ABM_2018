from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from sugarscape.agents import SsAgent, Sugar
from sugarscape.model import Sugarscape2ConstantGrowback
from sugarscape.model import HistogramModule

color_dic = {4: "#005C00",
             3: "#008300",
             2: "#00AA00",
             1: "#00F800"}


def SsAgent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is SsAgent:
        portrayal["Shape"] = "sugarscape/resources/ant.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Sugar:
        if agent.amount != 0:
            portrayal["Color"] = color_dic[agent.amount]
        else:
            portrayal["Color"] = "#D6F5D6"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

n_slider = UserSettableParameter("slider", "Numer of agents", 100, 2, 200, 1)
canvas_element = CanvasGrid(SsAgent_portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])
histogram = HistogramModule(list(range(10)), 200, 500)

server = ModularServer(Sugarscape2ConstantGrowback, [canvas_element, chart_element, histogram],
                       "Sugarscape 2 Constant Growback",
                       {"N": n_slider, "width": 50, "height": 50})
# server.launch()
