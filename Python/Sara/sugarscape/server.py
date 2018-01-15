from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from sugarscape.agents import SsAgent, Sugar
from sugarscape.model import Sugarscape2ConstantGrowback

color_dic = {10: "#042E04",
             9: "#064506",
             8: "#075907",
             7: "#097009",
             6: "#098209",
             5: "#0B9C0B",
             4: "#0DAB0D",
             3: "#0EC40E",
             2: "#0FD60F",
             1: "#11EB11"}


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


canvas_element = CanvasGrid(SsAgent_portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])

server = ModularServer(Sugarscape2ConstantGrowback, [canvas_element, chart_element],
                       "Sugarscape 2 Constant Growback")
# server.launch()
