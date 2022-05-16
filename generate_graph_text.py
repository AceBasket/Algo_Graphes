from random import randint

def is_in(list, X):
    for Z in list:
        if X == Z:
            return True
    return False

def generate_world(K, N):
    list_robots = []
    i = 0
    while i < K :
        x = randint(1, N)
        y = randint(1, N)
        if not is_in(list_robots, (x,y)):
            list_robots.append((x, y))
            i = i+1
    

    list_edges = []
    for robot1 in range(len(list_robots)):
        for robot2 in range(len(list_robots)):
            if robot1 != robot2:
                list_edges.append((robot1, robot2))

    return list_edges, list_robots

def generate_txt_file(K, N):
    list_edges, list_robots = generate_world(K, N)
    with open("random_graph.txt", 'w') as f:
        for i in range(len(list_robots)):
            line

