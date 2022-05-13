import graphviz
from text_to_graph import parse_graph_data

list_ids, robot_list, graph = parse_graph_data("graphe_intermediaire.txt")
with open("graphe.dot", 'w') as f:
    f.write("strict graph {")
    for i in range(len(list_ids)):
        line = '\n\t'
        if list_ids[i] == 0:
            line += 'R'
        elif list_ids[i] < 10:
            line += ("00"+str(list_ids[i]))
        elif list_ids[i] < 100:
            line += ('0'+str(list_ids[i]))
        else:
            line += str(list_ids[i])
        line += '[pos="'
        line += str(robot_list[i]["coord"][0])
        line += ','
        line += str(robot_list[i]["coord"][1])
        line += '!"color='
        if robot_list[i]["state"] == "awake":
            line += "green]"
        elif robot_list[i]["state"] == "asleep":
            line += "red]"
        elif robot_list[i]["state"] == "stand by":
            line += "blue]"
        f.write(line)
    for y in range(len(graph)):
        for x in range(y):
            if graph[y][x] > 0:
                line = '\n\t'

                id1 = str(robot_list[y]["id"])
                if id1 == '0':
                    id1 = 'R'
                else:
                    while len(id1) != 3:
                        id1 = '0'+id1
                line += id1

                line += "--"

                id2 = str(robot_list[x]["id"])
                if id2 == '0':
                    id2 = 'R'
                else:
                    while len(id2) != 3:
                        id2 = '0'+id2
                line += id2

                line += ""
                f.write(line)
    f.write("\n}")

        