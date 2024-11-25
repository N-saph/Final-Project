import matplotlib.pyplot as plt
import random


def generate_random_network(n, max_comparators):
    """Generates a random sorting network."""
    network = []
    for _ in range(max_comparators):
        i, j = random.sample(range(n), 2)
        network.append((min(i, j), max(i, j)))
    return network


def apply_network(arr, network):
    """Applies a sorting network to an array."""
    for i, j in network:
        if arr[i] > arr[j]:
            arr[i], arr[j] = arr[j], arr[i]
    return arr


def is_sorted(arr):
    """Checks if an array is sorted."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

def mutate(network, n):
    """Mutates the sorting network."""
    if random.random() < 0.5 and len(network) > 0:
        network.pop(random.randint(0, len(network) - 1)) 
    else:
        i, j = random.sample(range(n), 2)
        network.append((min(i, j), max(i, j))) 


def fitness(network, inputs):
    """
    Calculates the fitness of a sorting network based on its performance
    against a set of binary input test cases.
    """
    score = 0
    for test_case in inputs:
        output = apply_network(test_case[:], network)
        if is_sorted(output):
            score += 1
    return score / len(inputs) 


def evolve_inputs(n):
    """
    Generates all possible binary test cases of length n.
    """
    from itertools import product
    return [list(seq) for seq in product([0, 1], repeat=n)]


def evolve_network(n, max_comparators, generations, population_size):
    """
    Evolves a sorting network using co-evolving parasites.
    """
    network_population = [
        generate_random_network(n, max_comparators) for _ in range(population_size)
    ]
    input_population = evolve_inputs(n) 

    for gen in range(generations):
        network_population.sort(
            key=lambda net: fitness(net, input_population), reverse=True
        )
        top_networks = network_population[: population_size // 2]
        while len(network_population) < population_size:
            parent = random.choice(top_networks)
            child = parent[:]
            mutate(child, n)
            network_population.append(child)

        best_fitness = fitness(top_networks[0], input_population)
        print(f"Generation {gen + 1}: Best fitness = {best_fitness}")

        if best_fitness == 1.0:
            print("Optimal network found!")
            break

    return network_population[0]


def plot_network(network, n):
    """
    Plots the sorting network as a graph with lines and arrows.
    """
    plt.figure(figsize=(14, 8))

    for i in range(n):
        plt.plot([0, len(network)], [i, i], color="black", linewidth=0.5)

    for step, (i, j) in enumerate(network):
        x = step + 1
        plt.plot([x, x], [i, j], color="blue", linewidth=1.5)
        plt.scatter([x], [i], color="red", s=30) 
        plt.scatter([x], [j], color="green", s=30)

    plt.title("Sorting Network Visualization")
    plt.xlabel("Comparator Step")
    plt.ylabel("Input Lines")
    plt.xticks(range(0, len(network) + 1, 1))
    plt.yticks(range(0, n))
    plt.grid(axis="x", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    n = 16  
    max_comparators = 61
    generations = 100 
    population_size = 512 

    evolved_network = evolve_network(n, max_comparators, generations, population_size)

    test_array = random.sample(range(100), n)
    print(f"Original array: {test_array}")
    sorted_array = apply_network(test_array[:], evolved_network)
    print(f"Sorted array: {sorted_array}")
    print(f"Number of comparators: {len(evolved_network)}")

    assert sorted_array == sorted(test_array), "Array not sorted correctly!"

    plot_network(evolved_network, n)

