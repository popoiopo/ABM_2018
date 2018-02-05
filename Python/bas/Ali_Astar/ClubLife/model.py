# model.py
from mesa_own.space import MultiGrid
from mesa_own import Model
from mesa_own.time import BaseScheduler
from mesa_own.datacollection import DataCollector
from mesa_own.visualization.ModularVisualization import VisualizationElement

import random
import numpy as np

from ClubLife.agents import *
from ClubLife.AStar import *
from ClubLife.blocks import *


# ------------------Classes--------------------------
class Model(Model):
    '''
    ClubLife, an agent-based-model to simulate club related behaviour.
    '''
    def __init__(self, N, width, height, distance_coefficent=0, density_coefficent=10, density_vision=3):
        super().__init__()

        self.max_Astar = 0
        self.num_agents = N

        self.grid = MultiGrid(width, height, False)
        self.schedule = BaseScheduler(self)
        self.POI_cost = {}
        self.grid_density = [[0 for i in range(width)] for j in range(height)]

        self.serving_time = {'BAR': 3, 'BAR2': 3, 'BAR3': 3, 'BAR4': 3}

        # POI_points = [ (24, 49),(40, 7), (5, 7) ]
        # POI_names = ['STAGE', 'BAR', 'BAR2']

        # testing
        POI_points = [(24, 49), (24, 1)]
        POI_names = ['STAGE', 'BAR']

        # POI_points = [ (9, 33),(0, 5), (17, 5), (0,7),(17,7)]
        # POI_names = [ 'STAGE,'BAR1', 'BAR2','BAR3','BAR4']

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
            self.POI_cost[POI_names[r]] =\
              A_star_array(width, height, (x, y), self.blocks, distance_coefficent, 1)

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
                # x = 24
                # y = 1

                this_cell = self.grid.get_cell_list_contents((x, y))

                if (x, y) not in self.blocks and (x, y) not in selected_cells:

                    selected_cells.append((x, y))
                # for agent in this_cell:

                #     if type(agent) is nodeAgent:
                #         if (agent.block is False):
                #             notblock = True
                    break

            self.grid_density[x][y] += 1
            self.grid.place_agent(commuter, (24, 1))
            # self.grid.place_agent(commuter, (24, 49))
            # self.grid.place_agent(commuter, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={"utility": lambda a: a.utility, 'numOfPOIVisits': lambda a: a.numOfPOIVisits})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


class ChartModule(VisualizationElement):
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
