#Holland Mills, 2021
import csv
import random
import math
import numpy as np
from copy import deepcopy as dp
# create function to define an obstacles data structure
def find_obs(obs_path):
    with open(obs_path, newline='') as csvfile:
        obstacles = list(
            csv.reader(
                filter(lambda row: row[0] != '#', csvfile), dialect='excel', quotechar='|',
                quoting=csv.QUOTE_NONNUMERIC))
    return obstacles
#import the nodes and edges .CSVs to list while ignoring comments - converts to list format
def find_nodes():
    with open('../Results/nodes.csv', newline='') as csvfile:
        nodes_import = list(
            csv.reader(
                filter(lambda row: row[0] != '#', csvfile), dialect='excel'))
    return nodes_import
def find_edges():
    with open('../Results/edges.csv', newline='') as csvfile:
        edges_import = list(
            csv.reader(
                filter(lambda row: row[0] != '#', csvfile), dialect='excel'))
    return edges_import
np.seterr(divide='ignore', invalid='ignore')
# define a basic distance function that takes in two lists where the first two inputs are x y coordinates
def distance(p1, p2):
    d = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return d
# n is the number of partitions along both x and y axes
def make_c_free(n, xmin, xmax, ymin, ymax,obstacles_list):
    # create initial data structures
    x = np.linspace(xmin,xmax,n)
    y = np.linspace(ymin,ymax,n)
    x_1,y_1 = np.meshgrid(x,y)
    x_1 = x.tolist()
    y_1 = y.tolist()
    grid=list()
    c_free = dict()
    for i in range(len(x_1)):
         for j in range(len(y_1)):
             grid.append([x_1[i], y_1[j]])
    # convert grid to a dictionary data structure for easier
    # implementation during creation of c_free
    for i in range(len(grid)):
         if i not in c_free:
             c_free[str(i + 3)] = ()
         c_free[str(i + 3)] = grid[i]
    # create a copy of c_free to prevent errors with python pass by reference vs pass by value
    c_free_deep = dp(c_free)
    # create c_free by removing the roadmap nodes in the area of the objects
    for key, value in c_free_deep.items():
        for j in obstacles_list:
            if distance(value, j) <= j[2]/2:
                c_free.pop(key, None)
    return c_free
#collision detection function
def better_col(node1,node2,obj_list):
    p1 = np.array([node1[0],node1[1]])
    p2 = np.array([node2[0],node2[1]])
    v = np.subtract(p2,p1)
    a = np.dot(v,v)
    collsion_state = None
    for obst in obj_list:
        q = np.array([obst[0],obst[1]])
        r = obst[2]/2
        b = 2*np.dot(v,(np.subtract(p1,q)))
        c = np.dot(p1,p1)+np.dot(q,q)-2*np.dot(p1,q)-r**2
        discriminant = b**2-4*a*c
        if discriminant <0:
          continue
        sqrt_disc = math.sqrt(discriminant)
        t1=(-b + sqrt_disc)/(2*a)
        t2=(-b - sqrt_disc)/(2*a)
        if not(0<=t1 <=1 or 0<=t2 <=1):
          continue
        else:
          return 1
    return 0
#takes a list of edges and removes instances of collison
def clean_edges(list_of_edges):
    newlist = dp(list_of_edges)
    for i in range(len(newlist)):
        if newlist[i][3] == 1:
            list_of_edges.remove(newlist[i])
    return list_of_edges
    #key function for list sorting by cost,first_node
def get_cost(elem):
    return(elem[2])
def get_first(elem):
    return(elem[0])
#takes a list of edges, sorts them by cost and trims the edges to desired connections per node
def pruned_edges(edge_list,max_connections):
    edge_list.sort(key=lambda x:(x[0],x[2]))
    sorting_dict = dict()
    sorting_list = list()
    for each in edge_list:
        id1 = each[0]
        id2 = each[1]
        cost = each[2]
        if id1 not in sorting_dict:
            sorting_dict[id1] = dict()
        if id2 not in sorting_dict:
            sorting_dict[id2] = dict()
        sorting_dict[id1][id2] = cost
        sorting_dict[id2][id1] = cost
#take elements from dict, make a list for each key, sort it, trim it, then add to final list
    for node1,node2 in sorting_dict.items():
        temp_list = list()
        for key, value in node2.items():
            temp_list.append([node1,key,value])
        temp_list.sort(key=get_cost)
        del temp_list[max_connections:]
        sorting_list.extend(temp_list)
        sorting_list.sort(key=get_first)
    return sorting_list
def write_path_to_csv(path):
    with open('../Results/path.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(path)
def write_edges_to_csv(edges_list):
    header = ["# Each line below is of the form ID1 ID2 cost.","# where ID1 and ID2 are the IDs of the nodes connected by the edge and","# cost is the cost of traversing that edge (in either direction)."]
    with open('../Results/edges.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for i in header:
            writer.writerow([i])
        #Data add in csv file
        for x in edges_list:
            writer.writerow(x)
def write_nodes_to_csv(nodes_list):
    header = ["# Each line below has the form","# ID x y heuristic-cost-to-go","# where ID is the unique integer ID number of the node (1 through N)","# (x y) is the location of the node in the plane and heuristic-cost-to-go","# is an optimistic estimate of the path length from that node to the","# goal node as needed by A* search."]
    with open('../Results/nodes.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for i in header:
            writer.writerow([i])
        #Data add in csv file
        for x in nodes_list:
            writer.writerow(x)
def write_whatever_to_csv(whatever,output):
    with open(output,'w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for x in whatever:
            writer.writerow(x)
