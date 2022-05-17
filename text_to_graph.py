from math import ceil
import numpy as np

""" 
robot :
    dist : -1 by default, the distance to its objective otherwise
    coord : its coordinates
    dest : id of the robot which is its destination
    state : 0 for asleep ; 1 for awake ; 2 for in stand by
"""
def get_correct_index(list_ids, id):
    return list_ids.index(id)

def distance(A: tuple, B: tuple):
    return np.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)

def count_robot(lines):
    k = 0
    while k < len(lines) and (lines[k][0] == 'R' or (lines[k][0] <= '9' and lines[k][0] >= '0')):
        k += 1
    return k

def get_data_from_line(line):
    line = line.split(' : ')
    return list(filter(lambda c: c!= '(' and c != ')' and c!= '\n', line[1])), line

def parse_graph_data(text):
    with open(text, 'r') as f:
        lines = f.readlines()

    nb_robot = count_robot(lines)
    # print(nb_robot)
    robot_list = [None for k in range(nb_robot)]
    list_ids = []
    k = 0
    while k < nb_robot: # for each robot
        data, line = get_data_from_line(lines[k])
        # to get index for robot_list and id for robot

        id = ''
        for c in line[0]:
            id += c

        if id == 'R':
            list_index = 0
        else:
            list_index = int(id)
        list_ids.append(list_index)
        # to get robot coordinates
        i = get_correct_index(list_ids, list_ids[-1])
        robot_list[i] = None
        x = ''
        y = ''
        for c in data:
            if c != ',' and robot_list[i] == None:
                x += c
            elif c != ',':
                y += c
            else:
                robot_list[i] = 0 # so that robot isn't none
        robot_list[i] = {"dist": [], "coord": (int(x),int(y)), "dest": [], "state": "awake" if i == 0 else "asleep","range": None if i!=0 else "min" ,"id": list_index}
        k += 1


    # to get graph
    graph = np.zeros((nb_robot, nb_robot))
    for i in range(nb_robot):
        for j in range(nb_robot):
            dist = distance(robot_list[i]["coord"], robot_list[j]["coord"])
            graph[j][i] = ceil(dist) 
            graph[i][j] = ceil(dist)
            k += 1

    # graph = np.zeros((nb_robot, nb_robot))
    # while k < len(lines) and lines[k][0] == 'E':
    #     line = lines[k].split(' : ')
    #     data = list(filter(lambda c: c!= '(' and c != ')' and c!= '\n', line[1]))
    #     beg = True
    #     nb1 = ''
    #     nb2 = ''
    #     for c in data:
    #         if c == ',':
    #             beg = False
    #         elif beg:
    #             nb1 += c
    #         else:
    #             nb2 += c
    #     id1 =  0 if nb1 == 'R' else int(nb1)
    #     id2 =  0 if nb2 == 'R' else int(nb2)
    #     i = get_correct_index(list_ids, id1)
    #     j = get_correct_index(list_ids, id2)
    #     dist = distance(robot_list[i]["coord"], robot_list[j]["coord"])
    #     graph[j][i] = ceil(dist) 
    #     graph[i][j] = ceil(dist)
    #     k += 1


    return list_ids, robot_list, graph

if __name__ == "__main__":
    list_ids, robot_list, graph = parse_graph_data("mapK10.txt")
    print(list_ids)
    print(robot_list)
    print(graph)