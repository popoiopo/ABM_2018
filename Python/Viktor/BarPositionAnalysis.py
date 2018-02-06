from sugarscape.server import server
from mesa_own.batchrunner import BatchRunner
from sugarscape.agents import SsAgent, Sugar
from sugarscape.model import Sugarscape2ConstantGrowback
import numpy as np
import pandas
import matplotlib.pyplot as plt
import seaborn as sns

#server.launch()
# run.py


fixed_params = {"N": 750, "beta_c" : 1.9, "beta_d" : 1, "beta_w" : 0.5, "beer_consumption" : 0.0008333, "serving_speed" : 0.1, "height" : 34, "width" : 18}

variable_params = {"bar1_y": range(1, 33, 1)}
#variable_params = {"bar1_y": range(1, 33, 1), "bar2_y": range(1, 33, 1)}

batch_run = BatchRunner(Sugarscape2ConstantGrowback,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=1,
                        max_steps=1800,
                        model_reporters={"Waiting": lambda m: m.schedule.AverageWaitingTime(True), "MaxAgents": lambda m: m.schedule.MaxAgents()})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
print(run_data)

# Plot Results
plt.figure()
plt.plot(run_data['bar1_y'], run_data['MaxAgents'])
#dataC = run_data[['bar1_y', 'bar2_y', 'MaxAgents']]
#dataC = dataC.pivot(index='bar1_y', columns='bar2_y', values='MaxAgents')
#sns.heatmap(dataC)
plt.savefig("DataCrowd")
plt.figure()
plt.plot(run_data['bar1_y'], run_data['Waiting'])
#dataW = run_data[['bar1_y', 'bar2_y', 'Waiting']]
#dataW = dataW.pivot(index='bar1_y', columns='bar2_y', values='Waiting')
#sns.heatmap(dataW)
plt.savefig("DataWaiting")
plt.show()
