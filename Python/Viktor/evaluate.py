from sugarscape.server import server
from mesa_own.batchrunner import BatchRunner
from sugarscape.agents import SsAgent, Sugar
from sugarscape.model import Sugarscape2ConstantGrowback
import numpy as np
import pandas
import matplotlib.pyplot as plt

#server.launch()
# run.py

#def evaluate(values):



fixed_params = {"beta_c" : 1.9, "beta_d" : 1, "beta_w" : 0.5, "beer_consumption" : 0.0008333, "serving_speed" : 0.12, "height" : 34, "width" : 18, "bar1_y": 5, "bar2_y" : 6}

variable_params = {"N": range(500, 750, 260)}

batch_run = BatchRunner(Sugarscape2ConstantGrowback,
                        fixed_parameters=fixed_params,
                        variable_parameters = variable_params,
                        iterations=1,
                        max_steps=360,
                        model_reporters={"Waiting": lambda m: m.schedule.AverageWaitingTime(True)})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
print(run_data)
print(batch_run)
print(run_data.Waiting)
#plt.figure()
#plt.scatter(run_data.bar1_y, run_data.Waiting)
#plt.show()
