import numpy as np
from text_to_graph import parse_graph_data, get_correct_index
from rendering_graph import rendering
import sys 

""" ------------------ Utilities ------------------ """


def min(x,y):
    """ Returns a boolean x < y"""
    return x<y

def max(x,y):
    """ Returns a boolean x > y"""
    return x>y

def relacher_init(id,graph, id_List):
    """ Initializes 'd' and 'pere' arrays for the dijkstra algorithm"""
    d = []
    pere = []
    for j in range(len(graph)):
        d.append(np.inf)
        pere.append(0)
    d[get_correct_index(id_List,id)] = 0
    return (d, pere)

def relacher(i_u, i_v, d, pere, graph, id_List):
    """ Updates 'd' and 'pere' values for 'i_v' vertex modified by 'i_u' vertex"""
    if d[i_v] > d[i_u] + graph[i_u][i_v]:
        d[i_v] = d[i_u] + graph[i_u][i_v]
        pere[i_v] = id_List[i_u]

def not_Empty(tab):
    """ Boolean telling if there is a least one non-zero element in 'tab'"""
    for i in tab:
        if i == 1:
            return 1
    return 0

def ind_min(tab, Y):
    """ Returns the index of the minimum of 'tab'"""
    ind=0
    min= np.inf
    for i in range(len(tab)):
        if ((tab[i] < min) and (Y[i] == 1)):
            min = tab[i]
            ind = i
    return ind

def dijkstra(id, graph, id_List):
    """ Returns two arrays: \n 
     - 'd' is the distance to all other vertices starting from 'id' \n
     - 'pere' indicates the previous vertex to visit to reach'id'"""
    (d, pere) = relacher_init(id, graph, id_List)
    Y = [1 for k in range(len(graph))]
    while not_Empty(Y):
        u = ind_min(d, Y)
        Y[u] = 0
        for  v in range(len(graph[u])): 
            if Y[v] == 1 and graph[u][v]!= 0:
                relacher(u, v, d, pere, graph, id_List)
    return (d, pere)


""" ------------------ Robot functions ------------------ """


def robots_all_awake(robot_List):
    """ Checks if it remains at least one robot which is not awake"""
    for robot in robot_List:
        if robot["state"] != "awake":
            return 0
    return 1

def awake1(robot_List,id, graph, test, id_List):
    """ Wakes up 'id' robot and finds a destination far or close depending of 'test'"""
    robot_List[get_correct_index(id_List,id)]["state"] = "awake"
    robot_List[get_correct_index(id_List,id)]["range"] = test.__name__ # sets if this robot will look for close or far robots
    find_dest1(id, id, robot_List, test, graph, id_List)  # searchs robots to wake up

def awake_opti(robot_List,id, graph, test, id_List):
    """ Wakes up 'id' robot, resets his arrays 'dest' and 'dist', and finds a destination far or close depending of 'test' """
    robot_List[get_correct_index(id_List,id)]["state"] = "awake"
    robot_List[get_correct_index(id_List,id)]["range"] = test.__name__ # sets if this robot will look for close or far robots
    robot_List[get_correct_index(id_List,id)]["dest"] = [] # resets 'dest' array (which contained the id of the robot that woke him up)
    robot_List[get_correct_index(id_List,id)]["dist"] = [] # resets 'dist' array
    find_dest_opti(id, id, robot_List, test, graph, id_List) # searchs robots to wake up

def find_dest1(i, i_position, robot_List, test, graph, id_List):
    """ Updates the field "dest" of 'i' with the array of his destination and "dist" with the corresponding distances """
    dist,pere = dijkstra(i_position, graph, id_List) # dist = array of the distance to "id" , "pere" = array of ancestors to join "id"
    if test == min:
        test_dist = np.inf # sets the 'min' to infinity
    else:
        test_dist = 0 # sets the 'max' to 0
    ind = None
    for k in range(len(dist)):
        if test(dist[k], test_dist) and k != i_position and robot_List[k]["state"] == "asleep" : # searchs the closest or farthest sleeping robot
            test_dist = dist[k]
            ind = k
        
    if ind != None: 
        first_dest = id_List[ind]
        list_dest = [first_dest] # list_dest = road to follow to link "id" and the destination
        list_dist = [dist[get_correct_index(id_List, first_dest)]] # list_dist = list of the distance in relation with list_dest

        while pere[get_correct_index(id_List,first_dest)] != id_List[i_position]: # looks for all robots on the way
            first_dest = pere[get_correct_index(id_List,first_dest)]
            list_dest.append(first_dest)
            list_dist.append(dist[get_correct_index(id_List,first_dest)])

        for id in list_dest: # reservation of all robots on the way
            if robot_List[get_correct_index(id_List,id)]["state"] == "asleep":
                robot_List[get_correct_index(id_List,id)]["state"] = "reserved"
        list_dest = list_dest[::-1]
        list_dist = list_dist[::-1]

        robot_List[i]["dest"] = list_dest
        robot_List[i]["dist"] = list_dist


def reservation(robot_List, id_List, first_dest, i, list_dist):
    """ If the robot 'first_dest' is asleep : set the id of the robot that will wake him up (= i)
        If the robot 'first_dest' is reserved : change the reservation and erase it from the previous robot that had reserved him """
    if robot_List[get_correct_index(id_List, first_dest)]["state"] == "reserved" and list_dist[-1] < robot_List[get_correct_index(id_List, first_dest)]["dist"]:
        old_robot_id = robot_List[get_correct_index(id_List, first_dest)]["dest"][0] # id of the previous robot that had reserved the robot "first_dest"
        old_robot_res = len(robot_List[get_correct_index(id_List, old_robot_id)]["dest"]) # number of reservations that have the robot "old_robot"
        old_robot_obj = robot_List[get_correct_index(id_List, old_robot_id)]["dest"][old_robot_res-1] # final objective of the robot "old_robot"

        robot_List[get_correct_index(id_List, first_dest)]["dest"] = [i] # change the robot that reserve him...
        robot_List[get_correct_index(id_List, first_dest)]["dist"] = [list_dist[-1]] # ... and the distance associated

        # While the final objective of the "old_robot" isn't valid, take it off his road until it's get valid or only one destination remains
        while old_robot_res > 1 and (robot_List[get_correct_index(id_List, old_robot_obj)]["state"] == "awake" or robot_List[get_correct_index(id_List, old_robot_obj)]["dest"][0] != old_robot_id):
            robot_List[get_correct_index(id_List, old_robot_id)]["dest"].pop()
            robot_List[get_correct_index(id_List, old_robot_id)]["dist"].pop()
            old_robot_res = old_robot_res - 1
            old_robot_obj = robot_List[get_correct_index(id_List, old_robot_id)]["dest"][old_robot_res-1]

    elif robot_List[get_correct_index(id_List, first_dest)]["state"] == "asleep":
        robot_List[get_correct_index(id_List, first_dest)]["dest"] = [i]
        robot_List[get_correct_index(id_List, first_dest)]["dist"] = [list_dist[-1]]

def find_dest_opti(i, i_position, robot_List, test, graph, id_List):
    """ Updates the field "dest" of 'i' with the array of his destination and "dist" with the corresponding distances """
    dist,pere = dijkstra(i_position, graph, id_List) # dist = array of the distance to "id" , "pere" = array of ancestors to join "id"
    if test == min:
        test_dist = np.inf # sets the 'min' to infinity
    else:
        test_dist = 0 # sets the 'max' to 0
    ind = None
    for k in range(len(dist)):
        if test(dist[k], test_dist) and k != i_position and (robot_List[k]["state"] == "asleep" or (robot_List[k]["state"] == "reserved" and dist[k] < robot_List[k]["dist"][0])):
            # searchs the closest or farthest sleeping robot or a reserved robot that is closer to him than the incoming robot
            test_dist = dist[k]
            ind = k
        
    if ind != None: 
        first_dest = id_List[ind]
        list_dest = [first_dest] # list_dest = road to follow to link "id" and the destination
        list_dist = [dist[get_correct_index(id_List, first_dest)]] # list_dist = list of the distance in relation with list_dest
        reservation(robot_List, id_List, first_dest, i, list_dist)

        while pere[get_correct_index(id_List,first_dest)] != id_List[i_position]: # looks for all robots on the way
            first_dest = pere[get_correct_index(id_List,first_dest)]
            list_dest.append(first_dest)
            list_dist.append(dist[get_correct_index(id_List,first_dest)])
            reservation(robot_List, id_List, first_dest, i, list_dist)

        for id in list_dest: # reservation of all robots on the way
            if robot_List[get_correct_index(id_List,id)]["state"] == "asleep":
                robot_List[get_correct_index(id_List,id)]["state"] = "reserved"
        list_dest = list_dest[::-1]
        list_dist = list_dist[::-1]

        robot_List[i]["dest"] = list_dest
        robot_List[i]["dist"] = list_dist

def what_to_do1(i, robot_List, graph, id_List):
    """ First implementation of the algorithm for wakening the robot\n
    Strategy: The first robot will wake up the closest sleeping robot, which will wake up the farthest sleeping robot.
    the robot has a field (defined when awakened) that define if he looks for the closest or the farthest sleeping robot.
    When a robot that awake close robot wake up a robot, this robot will look for the farthest robot, and vice versa. The first awake robot will look for the closest.
    When a robot is going to wake up another robot, he will wake up all the sleeping robot on his way. All the robots he plans to wake up are reserved."""
    robot = robot_List[i]
    if robot["range"] == "min":
        state = max
        state_i = min
    else:
        state = min
        state_i = max
    awake1(robot_List, robot["dest"][0],graph, state, id_List) # wakes up the corresponding robot...
    id_dest = robot["dest"].pop(0) # ... erases him from the destinations...
    robot["dist"].pop(0) # ... erases also the distance...
    if len(robot["dest"]) == 0:
        find_dest1(robot["id"], id_dest, robot_List, state_i, graph, id_List) # ... and gives him a destination

def what_to_do_opti(i, robot_List, graph, id_List):
    """ Optimization of the previous algorithm\n
    Strategy: Now, when a robot is looking for a robot to wake up, he can take a reserved robot if he is closer to this robot
    than the robot that had reserved him."""
    robot = robot_List[i]
    if robot["range"] == "min":
        state = max
        state_i = min
    else:
        state = min
        state_i = max
    awake_opti(robot_List, robot["dest"][0],graph, state, id_List) # wakes up the corresponding robot...
    id_dest = robot["dest"].pop(0) # ... erases him from the destinations...
    robot["dist"].pop(0) # ... erases also the distance...
    if len(robot["dest"]) == 0:
        find_dest_opti(robot["id"], id_dest, robot_List, state_i, graph, id_List) # ... and gives him a destination

def move_Robots(robot_List, graph, what_to_do, id_List):
    """ Decreases all distances by 1 and, if necessary, wakes up a robot"""
    for robot in robot_List:
        if robot["state"] != "asleep" and len(robot["dist"]) > 0:
            for k in range(len(robot["dest"])): # decreases by 1 all the distance of "dist"
                robot["dist"][k] -=1
    for robot in robot_List:
        if len(robot["dist"]) >0 and robot["dist"][0] == 0 and robot["state"] == "awake": # If the smallest distance is 0...
            if robot_List[get_correct_index(id_List, robot["dest"][0])]["state"] != "awake": # If the robot reached isn't awake
                what_to_do(robot["id"], robot_List, graph, id_List)
            else:
                robot["dest"].pop(0) # erases the robot reached from the destinations
                robot["dist"].pop(0) # erases the distance associated


"""
We assume that the matrix graph is defined as follows:
     graph[i] is an array containing all the vertices linked to i and the element i,j is the weight associated with the edge (i,j)
We also have a robot_List array which contains all the robots (dictionaries) along with their fields:
     - "id"
     - "coord" (initialized at the start coordinates)
     - "state": asleep, awake, reserved
     - "dest" the array of destinations in order
     - "dist" the array of distances between the robot and its destination(s)
     - "range" the parameter dictating the strategy of the robot
"""

def main(text_graph): 
    """ The main function, calling all the others, and printing the amount of turns required to wake all robots"""
    id_List,robot_List, graph = parse_graph_data(text_graph)
    # rendering(id_List, robot_List, graph, 0)
    tour = 1
    find_dest_opti(0, 0, robot_List, min, graph, id_List)
    # rendering(id_List, robot_List, graph, tour)
    while not robots_all_awake(robot_List):
        tour +=1
        move_Robots(robot_List, graph, what_to_do_opti, id_List)
        # rendering(id_List, robot_List, graph, tour)
    print("Robots tous réveillés en ",tour,"tours.")
    return tour

if __name__ == "__main__":
    main(sys.argv[1])
