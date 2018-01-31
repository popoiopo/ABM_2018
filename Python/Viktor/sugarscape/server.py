from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa_own.visualization.modules import CanvasGrid
from mesa_own.visualization.ModularVisualization import ModularServer
from mesa_own.visualization.UserParam import UserSettableParameter

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

n_slider = UserSettableParameter("slider", "Number of agents", 1000, 1, 1500, 1)
beta_c = UserSettableParameter("slider", "Beta Crowd Penalty", 1.9, 0, 5, 0.1)        # Crowd
beta_d = UserSettableParameter("slider", "Beta Distance Penalty", 1, 0, 5, 0.1)        # Distance
beta_w = UserSettableParameter("slider", "Beta Waiting Time Penalty", 0.5, 0, 5, 0.1)    # Waiting Time
beer_consumption = UserSettableParameter("slider", "Beer Consumption Rate", 0.00083333, 0, 0.005, 0.00005)
serving_speed = UserSettableParameter("slider", "Serving Speed Bar", 0.20, 0, 1, 0.01)
#canvas_element = CanvasGrid(SsAgent_portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label": "Waiting", "Color": "#AA0000"}])

#server = ModularServer(Sugarscape2ConstantGrowback, [canvas_element, chart_element],
#"Sugarscape 2 Constant Growback")
grid = CanvasGrid(SsAgent_portrayal, 18, 34, 250, 500)

server = ModularServer(Sugarscape2ConstantGrowback,
                       [grid, chart_element],
                       "ABM Project",
                       {"N": n_slider, "beta_c": beta_c, "beta_d":beta_d, "beta_w": beta_w, "beer_consumption": beer_consumption, "serving_speed": serving_speed})

