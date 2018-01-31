from sugarscape.server import server
from mesa_own.batchrunner import BatchRunner
from sugarscape.agents import SsAgent, Sugar
from sugarscape.model import Sugarscape2ConstantGrowback
import numpy as np
import pandas
import matplotlib.pyplot as plt

#server.launch()
# run.py


fixed_params = {"N": 500, "beta_d" : 1, "beta_w" : 0.5, "beer_consumption" : 0.0008333, "serving_speed" : 0.05, "height" : 50, "width" : 50, "bar1_y" : 5, "bar2_y" : 6}

variable_params = {"beta_c": np.linspace(1.2, 3, 5)}

batch_run = BatchRunner(Sugarscape2ConstantGrowback,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=2,
                        max_steps=50,
                        model_reporters={"Waiting": lambda m: m.schedule.AverageWaitingTime(True)})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.figure()
plt.scatter(run_data.beta_c, run_data.Waiting)
plt.show()
