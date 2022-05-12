import numpy as np
from text_to_graph import parse_graph_data
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
    return x<y

def max(x,y):
    return x>y


def awake(robot_List,i, graph, test):
    robot_List[i]["state"] = "awake"
    find_Dest(i, i, robot_List, test, graph)

def relacher_init(i,graph):
    d = []
    pere = []
    for j in range(len(graph)):
        d.append(np.inf)
        pere.append(0)
    d[i] = 0
    return (d, pere)

def relacher(i_u, i_v, d, pere, graph):
    if d[i_v] > d[i_u] + graph[i_u][i_v]:
        d[i_v] = d[i_u] + graph[i_u][i_v]
        pere[i_v] = i_u

def not_Empty(tab):
    for i in tab:
        if i == 1:
            return 1
    return 0

def ind_min(tab, Y):
    ind=0
    min= np.inf
    for i in range(len(tab)):
        if ((tab[i] < min) and (Y[i] == 1)):
            min = tab[i]
            ind = i
    return ind

def ind_robot_id(robot_List, id):
    for ind in range(len(robot_List)):
        if robot_List[ind]["id"] == id:
            return ind
    return "wrong id"

def dijkstra(i, graph):
    (d, pere) = relacher_init(i, graph)
    Y = [1 for k in range(len(graph))]
    while not_Empty(Y):
        u = ind_min(d, Y)
        Y[u] = 0
        for  v in range(len(graph[u])): 
            if Y[v] == 1 and graph[u][v]!= 0:
                relacher(u, v, d, pere, graph)
    return (d, pere)

def find_Dest(i, i_position, robot_List, test, graph):
    dist,pere = dijkstra(i_position, graph) # dist = tableau des distances à id et père = tableau des antécedents pour relier à id
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
        first_dest = ind 
        list_dest = [first_dest] # list_dest = chemin à faire pour relier id à sa destination
        list_dist = [dist[first_dest]] # list_dist = list des distances associé à list_dest
        while pere[first_dest] != i_position:
            first_dest = pere[first_dest]
            list_dest.append(first_dest)
            list_dist.append(dist[first_dest])
        for id in list_dest: # On réserve tout les robots à reveiller en chemin
            if robot_List[id]["state"] == "asleep":
                robot_List[id]["state"] = "reserved"
        list_dest = list_dest[::-1]
        list_dist = list_dist[::-1]

        robot_List[i]["dest"] = list_dest
        robot_List[i]["dist"] = list_dist


def what_to_do1(i, robot_List, graph, state ):
    state = min
    robot = robot_List[i]
    awake(robot_List, robot["dest"][0],graph, max) # ...on réveille le robot correspondant...
    id_dest = robot["dest"].pop(0)
    robot["dist"].pop(0)
    if len(robot["dest"]) == 0:
        find_Dest(robot["id"], id_dest, robot_List, state, graph) # ...et on lui assigne sa destination

def what_to_do2(i,robot_List,graph, state):
    robot = robot_List[i]
    awake(robot_List, robot["dest"][0],graph, state) # ...on réveille le robot correspondant...
    id_dest = robot["dest"].pop(0)
    robot["dist"].pop(0)
    if len(robot["dest"]) == 0:
        find_Dest(robot["id"], id_dest, robot_List, min, graph) # ...et on lui assigne sa destination

def move_Robots(robot_List, graph, what_to_do):
    state = max
    for robot in robot_List:
        if robot["state"] == "awake" and len(robot["dist"]) > 0:
            for k in range(len(robot["dest"])): # On décremente de 1 toutes les distances de "dist"
                robot["dist"][k] -=1
            if robot["dist"][0] == 0:
                if robot_List[ind_robot_id(robot_List, robot["dest"][0])]["state"] != "awake": # Si la plus courte distance tombe à 0... 
                    what_to_do(robot["id"], robot_List, graph, state)
                    if state == max:
                        state = min
                    else:
                        state = max
                else:
                    robot["dist"].pop(0)
                    robot["dest"].pop(0)

def robots_all_awake(robot_List):
    for robot in robot_List:
        if robot["state"] != "awake":
            return 0
    return 1

def bjr(): 
    robot_list, graph = parse_graph_data("graphe.txt")
    tour = 1
    #print("graph: ", graph, "\n")
    # print("\n", tour)
    # for robot in robot_list:
    #     print(robot)
    find_Dest(0, 0, robot_list, min, graph)
    while not robots_all_awake(robot_list):
        tour +=1
        move_Robots(robot_list, graph, what_to_do2)
        # print("\n",tour)
        # for robot in robot_list:
        #     print(robot)
        # if tour >50:
        #     return 0
    print("Pour graphe.txt (aka le graphe du démon) avec méthode: what_to_do2")
    print("Robot tous réveillé en ",tour,"tours.")
    return 0

if __name__ == "__main__":
    bjr()
