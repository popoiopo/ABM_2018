# run.py
import numpy as np
import sys
import matplotlib.pyplot as plt

from server import server


server.port = 8528 # The default
server.launch()