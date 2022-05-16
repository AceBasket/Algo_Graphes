import matplotlib.pyplot as plt
from generate_graph_text import generate_world
from resolution import main

def plot_according_to_N(K):
    nbs_tour = []
    Ns = [i for i in range(0, 2000, 100)]
    for N in Ns:
        generate_world(K, N)
        nbs_tour.append(main("random_graph.txt"))

    # print(Ns)
    # print(nbs_tour)
    plt.plot(Ns, nbs_tour)
    plt.show()

if __name__ == "__main__":
    plot_according_to_N(100)
