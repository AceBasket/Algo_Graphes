import numpy as np
from text_to_graph import parse_graph_data, get_correct_index
"""
On suppose qu'on a la matrice graph défini comme suit:
    graph[i] est un tableau contenant l'ensemble des sommets reliés à i et l'élement i,j est le poids associé à l'arrete (i,j)
Nous avons également un tableau robot_List qui contient tous les robots (dictionnaires) ainsi que leurs champs:
    - id 
    - coord (initialisées au coordonées de départs)
    - state: asleep, awake, reserved
    - dest l'array des destination dans l'ordre
    - dist l'array des distances entre le robots et sa/ses destination/s

"""

def min(x,y):
    """ Returns a boolean x < y"""
    return x<y

def max(x,y):
    """ Returns a boolean x > y"""
    return x>y


def awake(robot_List,id, graph, test, id_List):
    """ Awaken 'id' robot and finds it a destination far or close depending of 'state'"""
    robot_List[get_correct_index(id_List,id)]["state"] = "awake"
    find_Dest(id, id, robot_List, test, graph, id_List)

def relacher_init(id,graph, id_List):
    """ Initialise 'd' and 'pere' array for the dijkstra algorithm"""
    d = []
    pere = []
    for j in range(len(graph)):
        d.append(np.inf)
        pere.append(0)
    d[get_correct_index(id_List,id)] = 0
    return (d, pere)

def relacher(i_u, i_v, d, pere, graph, id_List):
    """ Update 'd' and 'pere' values for 'i_v' vertex modified by 'i_u' vertex"""
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

def find_Dest(i, i_position, robot_List, test, graph, id_List):
    """ Update the field "dest" of 'i' with the array of its destination and "dist" with the corresponding distances """
    dist,pere = dijkstra(i_position, graph, id_List) # dist = tableau des distances à id et père = tableau des antécedents pour relier à id
    print(pere)
    if test == min:
        test_dist = np.inf
    else:
        test_dist =0
    ind = None
    for k in range(len(dist)):
        if test(dist[k], test_dist) and k != i_position and robot_List[k]["state"] == "asleep":
            test_dist = dist[k]
            ind = k
    if ind != None: 
        first_dest = id_List[ind] 
        list_dest = [first_dest] # list_dest = chemin à faire pour relier id à sa destination
        list_dist = [dist[get_correct_index(id_List, first_dest)]] # list_dist = list des distances associé à list_dest
        while pere[get_correct_index(id_List,first_dest)] != id_List[i_position]:
            first_dest = pere[get_correct_index(id_List,first_dest)]
            list_dest.append(first_dest)
            list_dist.append(dist[get_correct_index(id_List,first_dest)])
        for id in list_dest: # On réserve tout les robots à reveiller en chemin
            if robot_List[get_correct_index(id_List,id)]["state"] == "asleep":
                robot_List[get_correct_index(id_List,id)]["state"] = "reserved"
        list_dest = list_dest[::-1]
        list_dist = list_dist[::-1]

        robot_List[i]["dest"] = list_dest
        robot_List[i]["dist"] = list_dist


def what_to_do1(i, robot_List, graph, state, id_List):
    """ First implementation of the algorithm for wakening the robot\n
    Strategy: ???"""
    state = min
    robot = robot_List[i]
    awake(robot_List, robot["dest"][0],graph, max, id_List) # ...on réveille le robot correspondant...
    id_dest = robot["dest"].pop(0)
    robot["dist"].pop(0)
    if len(robot["dest"]) == 0:
        find_Dest(robot["id"], id_dest, robot_List, state, graph, id_List) # ...et on lui assigne sa destination

def what_to_do2(i,robot_List,graph, state, id_List):
    """ Second implementation of the algorithm for wakening the robot\n
    Strategy: ???"""
    robot = robot_List[i]
    awake(robot_List, robot["dest"][0],graph, state, id_List) # ...on réveille le robot correspondant...
    id_dest = robot["dest"].pop(0)
    robot["dist"].pop(0)
    if len(robot["dest"]) == 0:
        find_Dest(robot["id"], id_dest, robot_List, min, graph,id_List) # ...et on lui assigne sa destination

def move_Robots(robot_List, graph, what_to_do, id_List):
    """ Decrease all distances by 1 and, if necessary, wakes up a robot"""
    state = max
    for robot in robot_List:
        if robot["state"] == "awake" and len(robot["dist"]) > 0:
            for k in range(len(robot["dest"])): # On décremente de 1 toutes les distances de "dist"
                robot["dist"][k] -=1
            if robot["dist"][0] == 0:
                if robot_List[get_correct_index(id_List, robot["dest"][0])]["state"] != "awake": # Si la plus courte distance tombe à 0... 
                    what_to_do(robot["id"], robot_List, graph, state, id_List)
                    if state == max:
                        state = min
                    else:
                        state = max
                else:
                    robot["dist"].pop(0)
                    robot["dest"].pop(0)

def robots_all_awake(robot_List):
    """ Checks if it remains at least one robot which is not awake"""
    for robot in robot_List:
        if robot["state"] != "awake":
            return 0
    return 1

def main(): 
    """ The main function, calling all the others, and printing the amount of turns required to wake all robots"""
    id_List,robot_list, graph = parse_graph_data("petit_graphe.txt")
    # id_List,robot_list, graph = parse_graph_data("graphe_intermediaire.txt")
    # id_List,robot_list, graph = parse_graph_data("graphe_ultime.txt")
    tour = 1
    print("id: ", id_List, "\n")
    print("\n", tour)
    for robot in robot_list:
        print(robot)
    find_Dest(0, 0, robot_list, min, graph, id_List)
    while not robots_all_awake(robot_list):
        tour +=1
        move_Robots(robot_list, graph, what_to_do1, id_List)
        print("\n",tour)
        for robot in robot_list:
            print(robot)
        # if tour >2:
        #     return 0
    print("Pour graphe.txt (aka le graphe du démon) avec méthode: what_to_do1")
    print("Robot tous réveillé en ",tour,"tours.")
    return 0

if __name__ == "__main__":
    main()
