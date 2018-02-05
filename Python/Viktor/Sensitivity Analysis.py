import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np
from SALib.util import read_param_file
import os
from Script import evaluate


problem = {'names': ['N' , 'beta_c', 'beta_d', 'beta_w', 'serving_speed', 'bar1_y', 'bar2_y'],
    'num_vars': 7,
        'bounds': [[500, 750], [1.3, 2.5], [0.5, 1.5], [0.0, 1.0], [0.5, 2.0], [0, 33], [0, 33]]}
#problem = read_param_file('Values6.txt')


# Generate samples
param_values = saltelli.sample(problem, 5)

# Run model (example)
Y, Z = evaluate(param_values)

# Perform analysis
SiY = sobol.analyze(problem, Y, print_to_console=True)
SiZ = sobol.analyze(problem, Z, print_to_console=True)
# Returns a dictionary with keys 'S1', 'S1_conf', 'ST', and 'ST_conf'
# (first and total-order indices with bootstrap confidence intervals
