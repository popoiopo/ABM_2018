import matplotlib.pyplot as plt
from ClubLife.model_viz_Astar import *

# variable paramter: density_coefficent
# fixed paramters:  number of agents, grid_size, number of steps, vision for density

my_model = m_Model(100, 50, 50, distance_coefficent=0, density_coefficent=1, density_vision=2)

plt.grid(True)
plt.matshow(my_model.POI_cost['STAGE'])
plt.xlabel('x - location')
plt.ylabel('y - location')
plt.title('Coloration of the stage a-star with walls.')
plt.savefig("figures/Astar_coloration_stage_funnel")
plt.show()
plt.matshow(my_model.POI_cost['BAR'])
plt.xlabel('x - location')
plt.ylabel('y - location')
plt.title('Coloration of the bar a-star with walls.')
plt.savefig("figures/Astar_coloration_Bar_funnel")
plt.show()
