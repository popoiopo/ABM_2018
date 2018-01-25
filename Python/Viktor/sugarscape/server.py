from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from sugarscape.agents import SsAgent, Sugar
from sugarscape.model import Sugarscape2ConstantGrowback

color_dic = {5: "#E74C3C",
             4: "#ff9900",
             3: "#00bc8c",
             2: "#D6F5D6"}

def SsAgent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is SsAgent:
        portrayal["Shape"] = "sugarscape/resources/dot.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Sugar:
        if 1 < agent.amount < 6:
            portrayal["Color"] = color_dic[int(agent.amount)]
        elif agent.amount > 4:
            portrayal["Color"] = "#6f42c1"
        else:
            portrayal["Color"] = "#fff"
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
