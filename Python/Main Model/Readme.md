# An agent-based approach to model a nightlife venue.

## Summary

The model generates an 'nightlife venue' with agents, 'bar' grid cells and a stage grid cell.

An agents moves within the grid and has a beer_need counter which increases every time step, dependent on his beer_consumption parameter.
If beer_need is higher than a certain score, the agents switches from stage to bar mode.

Movement is based on a score function that analyses the gridcell within a set vision.
Dependent on the mode of the agent ( bar-mode or stage-mode) the agents score the cells
based on distance to the stage or bar, crowd (nr of agents) of the grid and crowd in front of the bar (only in bar-mode)

Once at the bar an agents is 'helped' within a number of timesteps, dependent on the serving_speed and the crowd in the 'bar' grid cell.
After being 'helped' an agents switches from bar-mode to stage-mode.

The waiting time of an agents is a counter that counts the amount of steps in beer-mode. It is set to zero after being 'helped'. The average waiting time is an output parameter of the model used for analysation of different bar arrangements and parameter settings. Maximum agents per grid cells is an output parameter as well.


The following parameters can be adjusted in the server:

serving_speed, beta_crowd, beta_waitingtime, beta_distance, population size,

The model is tests and demonstrates several Mesa concepts and features:
 - MultiGrid
 - Multiple agent types (ants, sugar patches)
 - Overlay arbitrary text (wolf's energy) on agent's shapes while drawing on CanvasGrid


## How to Run

To run the model interactively, run ``run.py`` in this directory. e.g.

```
    $ python Run.py
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

## Files

* ``sugarscape/agents.py``: Defines the SsAgent, and Sugar agent classes.
* ``sugarscape/schedule.py``: This is exactly based on wolf_sheep/schedule.py.
* ``sugarscape/model.py``: Defines the model itself
* ``sugarscape/server.py``: Sets up the interactive visualization server
* ``Run.py``: Launches a model visualization server.


## Data Analysis

 - For analyzation of bar position run BarPositionAnalysis.py
    This creates two plots that show the relation between the bar positions and the two output parameters (Waiting Time and Max Agents per gridcell)
 - For sensitivity analysis run Sensitivity Analysis.py
    This outputs the First, Second and Total order sensitivity indices of all the parameters mentioned before.
 
 
## Further Reading

This model is based on the Netlogo Sugarscape 2 Constant Growback:

Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.

The ant sprite is taken from https://openclipart.org/detail/229519/ant-silhouette, with CC0 1.0 license.
