import numpy as np

""" 
robot :
    dist : -1 by default, the distance to its objective otherwise
    coord : its coordinates
    dest : id of the robot which is its destination
    state : 0 for asleep ; 1 for awake ; 2 for in stand by
"""


def distance(A: tuple, B: tuple):
    return np.sqrt((A[0] + B[0])**2 + (A[1] + B[1])**2)

def count_robot(lines):
    k = 0
    while k < len(lines) and (lines[k][0] == 'R' or (lines[k][0] <= '9' and lines[k][0] >= '1')):
        k += 1
    return k

def get_data_from_line(line):
    line = line.split(' : ')
    return list(filter(lambda c: c!= '(' and c != ')' and c!= '\n', line[1])), line

def parse_graph_data(text):
    with open(text, 'r') as f:
        lines = f.readlines()

    nb_robot = count_robot(lines)
    robot_list = [None for k in range(nb_robot)];

    k = 0
    while k < nb_robot: # for each robot
        data, line = get_data_from_line(lines[k])

        # to get index for robot_list and id for robot
        if line[0] == 'R':
            list_index = 0
        elif line[0] <= '9' and line[0] >= '1':
            list_index = int(line[0])

        # to get robot coordinates
        robot_list[list_index] = None
        x = ''
        y = ''
        for c in data:
            if c != ',' and robot_list[list_index] == None:
                x += c
            elif c != ',':
                y += c
            else:
                robot_list[list_index] = 0 # so that robot isn't none
        robot_list[list_index] = {"dist": [], "coord": (int(x),int(y)), "dest": [], "state": "awake" if list_index == 0 else "asleep", "id": list_index}
        k += 1


    # to get graph
    graph = np.zeros((nb_robot, nb_robot))
    while k < len(lines) and lines[k][0] == 'E':
        line = lines[k].split(' : ')
        data = list(filter(lambda c: c!= '(' and c != ')' and c!= '\n', line[1]))
        i =  0 if data[0] == 'R' else int(data[0])
        j =  0 if data[2] == 'R' else int(data[2])
        dist = distance(robot_list[i]["coord"], robot_list[j]["coord"])
        graph[j][i] = int(dist) + 1 
        graph[i][j] = int(dist) + 1
        k += 1


    return robot_list, graph

if __name__ == "__main__":
    robot_list, graph = parse_graph_data("graphe.txt")
    print(robot_list)
    print(graph)