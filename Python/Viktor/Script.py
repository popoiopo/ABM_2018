from sugarscape.server import server
from mesa_own.batchrunner import BatchRunner
from sugarscape.agents import SsAgent, Sugar
from sugarscape.model import Sugarscape2ConstantGrowback
import numpy as np
import pandas
import matplotlib.pyplot as plt


def evaluate(values):

    Y = np.zeros([values.shape[0]])
    Z = np.zeros([values.shape[0]])
    
    
    for i, X in enumerate(values):

        fixed_params = {"N" : int(X[0]), "beta_d" : X[2], "beta_w" : X[3], "beer_consumption" : 0.0008333, "serving_speed" :X[4], "height" : 34, "width" : 18, "bar1_y": int(X[5]), "bar2_y" : int(X[6])}
        variable_params = {"beta_c": np.linspace(X[1],3.0,1)}
     
        batch_run = BatchRunner(Sugarscape2ConstantGrowback, fixed_parameters=fixed_params,     variable_parameters = variable_params, iterations=1, max_steps=1800, model_reporters={"Waiting": lambda m: m.schedule.AverageWaitingTime(True), "MaxAgents": lambda m: m.schedule.MaxAgents()})
        batch_run.run_all()
      
        run_data = batch_run.get_model_vars_dataframe()
        #Y = run_data.Waiting
        Y[i] = run_data.Waiting
        Z[i] = run_data.MaxAgents
    
    
    return Y, Z



