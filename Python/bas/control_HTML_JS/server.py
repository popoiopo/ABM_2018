from mesa_own.visualization.ModularVisualization import ModularServer
from mesa_own.visualization.modules import CanvasGrid, ChartModule
import random
import randomcolor
from agents import SsAgent, Sugar
from model import Sugarscape2ConstantGrowback
from mesa_own.visualization.UserParam import UserSettableParameter

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
    rand_color = randomcolor.RandomColor()

    if type(agent) is SsAgent:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.9
        portrayal["filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["Color"] = rand_color.generate()

    elif type(agent) is Sugar:
        if agent.amount > 1.0:
            portrayal["Color"] = color_dic[random.randint(1,10)]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


n_slider = UserSettableParameter("slider", "Numer of agents", 100, 2, 200, 1)
domain_size = UserSettableParameter("slider", "GridSize", 50, 25, 250, 1)
canvas_element = CanvasGrid(SsAgent_portrayal, domain_size.value, domain_size.value, 500, 500)
chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])

server = ModularServer(Sugarscape2ConstantGrowback, [canvas_element, chart_element],
                       "ClubLife",
                       {"N": n_slider, "domain_size": domain_size})
# server.launch()
