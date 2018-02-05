import matplotlib.pyplot as plt
from ClubLife.model_viz_Astar import *

# variable paramter: density_coefficent
# fixed paramters:  number of agents, grid_size, number of steps, vision for density
print("hallo")

my_model = Model("N": n_slider, "width": domain_size, "height": domain_size, distance_coefficent=0, density_coefficent=1, density_vision=2)

plt.grid(True)
plt.matshow(my_model.POI_cost['STAGE'])
plt.savefig("figures/Astar_coloration_stage_funnel")
plt.show()
plt.matshow(my_model.POI_cost['BAR'])
plt.savefig("figures/Astar_coloration_Bar_funnel")
plt.show()
