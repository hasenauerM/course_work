#Holland Mills - A* Function - March, 2021
import csv
import numpy as np
import math
import aux_func as af
#define the find_path function which finds the parents of each node starting at goal and ending at start
def find_path(node,parents):
  found_path = [node]
  while node in parents:
    found_path.append(int(parents[node]))
    node = parents[node]
 #reverse the list to return in order from start to goal
  found_path.reverse()
  return found_path
#define a function  that determines if a node is in open and either inserts to OPEN or updates OPEN and then sorts OPEN
def maybe_insert_and_sort(node, sorted_nodes,oc_dict,pc_dict):
    if node not in sorted_nodes:
      sorted_nodes.append(node)
    sorted_nodes.sort(key=lambda node: oc_dict[node]+pc_dict[node])
#all_star_function
def all_star(roadmap_graph):
#create empty data structures for later implementation with imported csv data
    optimistic_cost = dict()
    past_cost = dict()
    parents_dict = dict()
#import data from imported node CSV data
    nodes_import = af.find_nodes()
    edges_import = af.find_edges()
    for node in nodes_import:
#create optimistic cost and past cost data structures
        optimistic_cost[int(node[0])]=float(node[3])
        past_cost[int(node[0])] = math.inf
    past_cost[1] = 0
#this version of setting goal allows for csv files longer than the examples provided in the course
    goal = len(nodes_import)
    #set up initalization before the algorithm
    OPEN = [1]
    CLOSED = []
# A* Algorithm
    while OPEN != []:
      current = OPEN.pop(0)
      CLOSED.append(current)
      if 1 not in roadmap_graph:
          print('FAILURE')
          break
      if current == goal:
        print('SUCCESS!')
        path = find_path(current,parents_dict)
        print("Shortest path to goal is: ")
        print(path)
        af.write_path_to_csv(path)
        break
      for nbr, cost in roadmap_graph[current].items():
        if nbr in CLOSED:
          next
        tpc = past_cost[current]+cost
        if tpc < past_cost[nbr]:
          past_cost[nbr]=tpc
          parents_dict[nbr] = current
          maybe_insert_and_sort(nbr,OPEN,optimistic_cost,past_cost)
    else:
      print('FAILURE')
