#import auxiliary functions
import aux_func as af
import a_star as star
import random
import math
from copy import deepcopy as dp
import itertools
import numpy as np
#creates a list of points with new node IDs from C_free
def grab_points(c_f, n):
  g_map = list()
  sam_pts = random.sample(c_free.items(), n)
  for i in range(len(sam_pts)):
    id = i+2
    x_pos = sam_pts[i][1][0]
    y_pos = sam_pts[i][1][1]
    g_map.append([id,x_pos,y_pos,af.distance((x_pos,y_pos),goal_pos)])
  return g_map
#insert function purpose here
def a_star_prep(roadmap, g_node):
    for key, value in roadmap.items():
      optimistic_cost[key] = af.distance(value, g_node)
      past_cost[key] = math.inf
    past_cost[1] = 0
#create a list of edges with selected nodes and check for collision
def find_edges(list_of_nodes,obj_list):
    edgies = list()
    for a, b in itertools.combinations(list_of_nodes, 2):
        node1 = [a[1],a[2]]
        node2 = [b[1],b[2]]
        edgies.append([a[0],b[0],af.distance(node1,node2),af.better_col(node1,node2,obj_list)])
        edgies = af.clean_edges(edgies)
    return edgies
#creates a graph using list of edges
def edges_to_graph(list_of_edges):
    graph = dict()
    for edge in list_of_edges:
        id1=edge[0]
        id2=edge[1]
        cost = edge[2]
        if id1 not in graph:
            graph[id1] = dict()
        if id2 not in graph:
            graph[id2] = dict()
        graph[id1][id2] = cost
        graph[id2][id1] = cost
    return graph
#import obstacles list
obstacles = af.find_obs('../Results/obstacles.csv')
#create c_free
c_free = af.make_c_free(100, -.5, .5, -.5, .5,obstacles)
#create base prm nodes and insert start and goal nodes
start_pos = [-0.5,-0.5]
goal_pos = [.5,.5]
sample_pts = grab_points(c_free,15)
#set start and goal points
start = 1
goal = len(sample_pts)+2
sample_pts.append([start,start_pos[0],start_pos[1],af.distance(start_pos,goal_pos)])
sample_pts.append([goal,goal_pos[0],goal_pos[1],0])
sample_pts.sort(key=af.get_first)
edges = find_edges(sample_pts,obstacles)
edges = af.pruned_edges(edges,3)
graphic = edges_to_graph(edges)
af.write_edges_to_csv(edges)
af.write_nodes_to_csv(sample_pts)
g = star.all_star(graphic)
