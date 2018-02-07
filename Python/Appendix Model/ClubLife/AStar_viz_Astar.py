from ClubLife.agents import *


def get_neighbours(cost_list, pos):

    """
    This function takes the current_postion, and a 2D array with the same dimension as the grid's
    and returns the coordinates of the agent's neighbouring cells

    Args:
        cost_list :=  a 2D array with the same dimension as the grid's
        pos := the current position of the agent 

    Returns:
        the list of the coordinates of the agent's neighbouring cells
    """



    x = pos[0]
    y = pos[1]
    neighbours = []

    x_max = len(cost_list) - 1
    x_min = 0

    y_max = len(cost_list[0]) - 1
    y_min = 0

    # right
    if x_max >= x+1:
        neighbours.append((x+1, y))

    # left
    if x_min <= x-1:
        neighbours.append((x-1, y))

    # top
    if y_max >= y+1:
        neighbours.append((x, y+1))

    # bottom
    if y_min <= y-1:
        neighbours.append((x, y-1))

    #  upper right corner
    if x_max >= x+1 and y_max >= y+1:
        neighbours.append((x+1, y+1))

    # upper left corner
    if x_min <= x-1 and y_max >= y+1:
        neighbours.append((x-1, y+1))

    # lower left corner
    if x_min <= x-1 and y_min <= y-1:
        neighbours.append((x-1, y-1))

    # lower right corner
    if x_max >= x+1 and y_min <= y-1:
        neighbours.append((x+1, y-1))

    return neighbours


def A_star_array(grid_width, grid_height, location_point, blocks, distance_coefficent=0, m_range_coefficent=1):
    """
    This function calculates the cost of reaching to a POI from every other cells in the grid, and stores the 
    result within a 2D array accesible by every agent.

    Args:
        grid_width :=   the width of the grid
        grid_height :=  the height of the grid
        location_point :=  the cooridnate of the POI
        blocks := the list of cooridnates of the blocks
        distance_coefficent := the coefficent of euclidean distance
        m_range_coefficent :=  the coeffenit  of dikstra cost

    Returns:
        a 2D array, where each cell stores the cost of moving to the given POI
    """


    pos = location_point
    node_list = []
    check_list = []

    cost_list = [[-1 for i in range(grid_width)] for j in range(grid_height)]
    print("test")
    for block_pos in blocks:
        cost_list[block_pos[0]][block_pos[1]] = -1

    cost_list[pos[0]][pos[1]] = 0

    node_list.append((pos, 0))
    check_list.append(pos)

    while(True):

        # find the neighbouring positions
        this_node = node_list.pop(0)
        pos = this_node[0]
        m_range = this_node[1]

        neighbor_positions = get_neighbours(cost_list, pos)

        for ps in neighbor_positions:

            if (ps not in blocks) and (ps not in check_list):

                check_list.append(ps)
                #node_list.append((ps, m_range+ get_distance(ps,pos)))
                node_list.append((ps, m_range + 1))

        dist = get_distance(location_point, pos)
        cost_list[pos[0]][pos[1]] = (m_range_coefficent * m_range) + (distance_coefficent * dist)

        if len(node_list) == 0:

            return cost_list


def A_star_node(self, location_point, location_name, blocks, distance_coefficent, m_range_coefficent):

    """
    This function calculates the cost of reaching to a POI from every other cells in the grid, and stores the 
    result within the node agents, this function is used for visualization purposes.
    Args:
        grid_width :=   the width of the grid
        grid_height :=  the height of the grid
        location_point :=  the cooridnate of the POI
        blocks := the list of cooridnates of the blocks
        distance_coefficent := the coefficent of euclidean distance
        m_range_coefficent :=  the coeffenit  of dikstra cost

    """


    pos = location_point
    node_list = []
    check_list = []
    max_list = []

    this_cell = self.grid.get_cell_list_contents(pos)
    for agent in this_cell:
        if type(agent) is nodeAgent and agent.block is False:
            check_list.append(pos)
            node_list.append((pos, 0))
            agent.locations[location_name] = 0
            max_list.append(0)

    while(True):

        # find the neighbouring positions
        this_node = node_list.pop(0)
        pos = this_node[0]
        m_range = this_node[1]

        neighbor_positions = self.grid.get_neighborhood(
            pos,
            moore=True,
            include_center=False)

        # for each neighbouring positions, get the contents of that postion
        for i in range(len(neighbor_positions)):
            this_cell = self.grid.get_cell_list_contents(neighbor_positions[i])

            if not (neighbor_positions[i] in check_list) and neighbor_positions[i] not in blocks:

                node_list.append((neighbor_positions[i], m_range+1))
                check_list.append(neighbor_positions[i])

            # get the node agent, assign to its location value of i, which refers to the range of moore neighbourhood
            for agent in this_cell:
                if type(agent) is nodeAgent:

                    dist = get_distance(location_point, neighbor_positions[i])
                    agent.locations[location_name] = (m_range_coefficent * m_range) + (distance_coefficent * dist)

        if len(node_list) == 0:
            return
