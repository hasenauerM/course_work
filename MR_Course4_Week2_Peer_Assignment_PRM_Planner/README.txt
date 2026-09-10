#Sampling_Based_Planning_Readme
Info:
Written in Python by Holland Mills, March 2021
Uses a PRM planner
Uses the following libraries:
csv, random, math, itertools, copy, numpy


Description:
Creates c_free from obstacles.csv and a fixed xmin,xmax,ymin,ymax (prm.py: line 51).

Resolution of nodes is determined by first input to make_c_free (prm.py: line 51,aux_func.py: line 34).

Nodes in contact with an object are removed from c_free.

A sample of nodes in c_free are taken uniformly, renumbered 3 to n (to work with coppelia) and the sample has goal and end nodes appended as nodes 1 & 2. This is then sorted (again, to work with coppelia).

Edges are found between each node in the sample (prm.py: line 32), a collision detection algorithm is used to determine if an edge is in collision with an obstacle (aux_func.py: lines 61-82).

List of Edges are then cleaned up to remove collisions, sorted by node and distance between parent node, and then trimmed to a set number of neighbors (aux_func.py: lines 96-119)

Edges are then converted into a graph using edges_to_graph (prm.py: line 35).

Edges and nodes are written to .csv files for use with A* algorithm from previous project converted to work as a function(a_star.py).

A* is used on graph, imports the written .csv files and outputs solution to path planning problem or FAILURE if no path is found.
