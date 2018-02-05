# Agent-Based-Modeling
## ClubLife

Welcome to `ClubLife` where crowddynamics and agent-based-modelling meet. In this repository you will find lots of run files in its root directory. These run files all refer to files that are either within the ClubLife, ClubLife_no_walls or mesa_own folders. This distinction has been done to be able to run different scenario's of the model, without ever changing parameters within the code.

In the figures folder, all the outcomes of the experiments are shown (the output of all the exp\*.py files.) Furthermore there is a two part reason for the Mesa library to be loaded in locally. The first is because this nullifies the need for a used to download mesa through pip. And second but most important, the standard JavaScript and HTML templates that are usually used by Mesa did not meet our demands, so changes within the source code of the Mesa library were made. Especially within the modular_template.html file.


| Variable | Funnel | No Walls |
| ---- | ----------------- | -------------------|
| Floor PLans | ![](figures/floorplan_no_walls.JPG) | ![](figures/Astar_coloration_Bar_no_walls.png) |
| Density Coefficient | ![](figures/DifferentDensityCoefficent.png) | ![](figures/DifferentDensityCoefficent_no_walls.png)|
| Number of Agents | ![](figures/DifferentNumOfAgents.png) | ![](figures/DifferentNumOfAgents_no_blocks.png)|
| Vision | ![](figures/DifferentVisions-d1-n200.png) | ![](figures/DifferentVisions-d1-n200_no_walls.png)|
| All of the above | ![](figures/Differentvis_den_numagents.png) | ![](figures/Differentvis_den_numagents_no_blocks.png)|