import matplotlib.pyplot as plt
from ClubLife_no_walls.model_viz_Astar import *

# variable paramter: density_coefficent
# fixed paramters:  number of agents, grid_size, number of steps, vision for density


my_model = Model(100, 50, 50, distance_coefficent=0, density_coefficent=1, density_vision=2)

plt.grid(True)
plt.matshow(my_model.POI_cost['STAGE'])
plt.xlabel('x - location')
plt.ylabel('y - location')
plt.title('Coloration of the stage a-star with walls.')
plt.savefig("figures/Astar_coloration_stage_no_walls")
plt.show()
plt.matshow(my_model.POI_cost['BAR'])
plt.xlabel('x - location')
plt.ylabel('y - location')
plt.title('Coloration of the left bar a-star with walls.')
plt.savefig("figures/Astar_coloration_Bar_no_walls")
plt.show()
plt.matshow(my_model.POI_cost['BAR2'])
plt.xlabel('x - location')
plt.ylabel('y - location')
plt.title('Coloration of the right bar a-star with walls.')
plt.savefig("figures/Astar_coloration_Bar2_no_walls")
plt.show()
