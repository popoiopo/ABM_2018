# model.py
from mesa_own.space import MultiGrid
from mesa_own import Model
from mesa_own.time import BaseScheduler
from mesa_own.datacollection import DataCollector
from mesa_own.visualization.ModularVisualization import VisualizationElement

import random
import numpy as np

from ClubLife.agents import *
from ClubLife.AStar_viz_Astar import *
from ClubLife.blocks_viz_Astar import *


# ------------------Classes--------------------------
class m_Model(Model):
    """ This class is the main model which inherits the Model class in Mesa   

    Attributes:
        max_Astar:= maximum value of cost from A_star algorithm, used for visualization
        num_agents:= total number of agents
        POI_cost:= a dictionary where the keys hold the POI_names and the values are a 2D arrary holding 
        the cost value of reaching to that POI 
        grid_density:= a 2D arrary that stores the number of agents in each cell of the grid, and 
        is updated within every movement of the agents.
        service_time:= stores the service time at the servicable POIs 
    """

    def __init__(self, N, width, height, distance_coefficent=0, density_coefficent=10, density_vision=3):
        super().__init__()

        self.max_Astar = 0
        self.num_agents = N

        self.grid = MultiGrid(width, height, False)
        self.schedule = BaseScheduler(self)
        self.POI_cost = {}
        self.grid_density = [[0 for i in range(width)] for j in range(height)]

        self.serving_time = {'BAR': 3, 'BAR2': 3, 'BAR3': 3, 'BAR4': 3}

        POI_points = [(24, 49), (24, 1)]
        POI_names = ['STAGE', 'BAR']

        POI_dict = {}
        for i in range(len(POI_points)):
            POI_dict[POI_names[i]] = POI_points[i]

        for i in range(width):
            for j in range(height):

                nd = nodeAgent((i, j), self, POI_names)
                self.grid.place_agent(nd, (i, j))

        self.blocks = block_positions
        create_block(self, block_positions, POI_names)
        create_POI(self, POI_points, 2)

        for r in range(len(POI_points)):

            x = POI_points[r][0]
            y = POI_points[r][1]

            A_star_node(self, (x, y), POI_names[r], self.blocks, 0.5, 2)
            self.POI_cost[POI_names[r]] = A_star_array(width, height, (x, y), self.blocks, distance_coefficent, 1)

        commuters_list = []
        for k in range(self.num_agents):
            a = commuterAgent(k, self, POI_dict, density_coefficent, density_vision)
            commuters_list.append(a)


        selected_cells = []
        for commuter in commuters_list:

            self.schedule.add(commuter)

            notblock = False
            selected_cell = False
            while(True):

                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)

                this_cell = self.grid.get_cell_list_contents((x, y))

                if (x, y) not in self.blocks and (x, y) not in selected_cells:

                    selected_cells.append((x, y))
                    break

            self.grid_density[x][y] += 1
            self.grid.place_agent(commuter, (24, 1))

        self.datacollector = DataCollector(
            agent_reporters={"utility": lambda a: a.utility, 'numOfPOIVisits': lambda a: a.numOfPOIVisits})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


class ChartModule(VisualizationElement):
    """ This class is used for chart visualization

    Attributes:
        canvas_height 
        canvas_width 
        WaitingTime
    """

    package_includes = ["Chart.min.js"]
    local_includes = ["js/LineChartModule.js"]

    def __init__(self, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.WaitingTime = []
        new_element = "new ChartModule({}, {})"
        new_element = new_element.format(canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        wait = [agent.WaitingTime for agent in model.schedule.agents]
        wait = list(filter(lambda a: a != 0, wait))
        try:
            self.WaitingTime.append(int(sum(wait) / len(wait)))
        except ZeroDivisionError:
            self.WaitingTime.append(0)
        return self.WaitingTime


class ChartModuleUtil(VisualizationElement):
    """ This class is used for chart visualization

    Attributes:
        canvas_height 
        canvas_width 
        utility
    """

    package_includes = ["Chart.min.js"]
    local_includes = ["js/LineChartModuleUtil.js"]

    def __init__(self, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.utility = []
        new_element = "new ChartModuleUtil({}, {})"
        new_element = new_element.format(canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        util = [agent.util for agent in model.schedule.agents]
        # visits = [agent.numOfPOIVisits for agent in model.schedule.agents]
        self.utility.append(sum(util) / len(util))
        return self.utility


class HistogramModule(VisualizationElement):
    """ This class is used for histogram visualization

    Attributes:
        canvas_height 
        canvas_width 
        bins
    """
    package_includes = ["Chart.min.js"]
    local_includes = ["js/HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        beers = [agent.numOfPOIVisits for agent in model.schedule.agents]
        hist = np.histogram(beers, bins=self.bins)[0]
        return [int(x) for x in hist]
