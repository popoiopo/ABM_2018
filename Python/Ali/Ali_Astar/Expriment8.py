
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


import model
import agents

# variable paramter: density_coefficent
# fixed paramters:  number of agents, grid_size, number of steps, vision for density


my_model = model.Model(100, 50,50,distance_coefficent= 0 ,density_coefficent=1,density_vision= 2)



plt.grid(True)
plt.matshow(my_model.POI_cost['STAGE'])
plt.savefig("Experiment8_stage")
plt.show()
plt.matshow(my_model.POI_cost['BAR'])
plt.savefig("Experiment8_Bar")

plt.show()
plt.matshow(my_model.POI_cost['BAR2'])
plt.savefig("Experiment8_Bar2")

plt.show()
