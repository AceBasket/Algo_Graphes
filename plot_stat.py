import matplotlib.pyplot as plt
from generate_graph_text import generate_txt_file
from resolution import main

def plot_according_to_N(K):
    nbs_tour = []
    Ns = [i for i in range(100, 1000, 100)]
    for N in Ns:
        value = 0
        for i in range(10):
            generate_txt_file(K, N)
            value += main("random_graph.txt")
        nbs_tour.append(value/10)
        
    plt.bar(Ns, nbs_tour, width=10)
    plt.xlabel("Taille du monde")
    plt.ylabel("Nombre d'itérations en moyenne")
    plt.title("Evolution du nombre d'itérations en fonction de la taille du monde avec " + str(K) + " robots")
    plt.show()

def plot_according_to_K(N):
    nbs_tour = []
    Ks = [i for i in range(10, 20, 2)]
    for K in Ks:
        value = 0
        for i in range(10):
            generate_txt_file(K, N)
            value += main("random_graph.txt")
        nbs_tour.append(value/10)

    plt.bar(Ks, nbs_tour)
    plt.xlabel("Nombre de robots")
    plt.ylabel("Nombre d'itérations")
    plt.title("Evolution du nombre d'itérations en fonction du nombre de robots avec un monde de taille " + str(N) + "x"+ str(N))
    plt.show()
    

def plot_world1000_K_changing():
    nbs_tour = []
    Ks = [10, 50, 200, 1000]
    for K in Ks:
        value = 0
        for i in range(10):
            generate_txt_file(K, 1000)
            value += main("random_graph.txt")
        nbs_tour.append(value/10)

    plt.bar(Ks, nbs_tour)
    plt.xlabel("Nombre de robots")
    plt.ylabel("Nombre d'itérations en moyenne")
    plt.title("Evolution du nombre d'itérations en fonction du nombre de robots avec un monde de taille 1000x1000")
    plt.show()

if __name__ == "__main__":
    plot_according_to_N(10)
    plot_according_to_K(50)
    plot_world1000_K_changing()
