import matplotlib.pyplot as plt
import random


def generate_random_network(n, max_comparators):
    """
    Generate a random sorting network.
    
    Parameters:
    - n (int): Number of input elements.
    - max_comparators (int): Maximum number of comparators.
    
    Returns:
    - list: Randomly generated sorting network.
    """
    network = []
    for _ in range(max_comparators):
        i, j = random.sample(range(n), 2)
        network.append((min(i, j), max(i, j)))
    return network


def apply_network(arr, network):
    """
    Apply a sorting network to an array.
    
    Parameters:
    - arr (list): The array to sort.
    - network (list of tuples): The sorting network (comparators).
    
    Returns:
    - list: The sorted array.
    """
    for i, j in network:
        if arr[i] > arr[j]:
            arr[i], arr[j] = arr[j], arr[i]
    return arr


def is_sorted(arr):
    """Check if the array is sorted."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def fitness(network, n):
    """
    Evaluate the fitness of a sorting network.
    
    Parameters:
    - network (list of tuples): The sorting network.
    - n (int): Number of inputs.
    
    Returns:
    - int: Number of successfully sorted test cases.
    """
    score = 0
    for _ in range(1000):
        arr = random.sample(range(100), n)
        sorted_arr = apply_network(arr[:], network)
        if is_sorted(sorted_arr):
            score += 1
    return score


def mutate(network, n):
    """
    Mutate a sorting network.
    
    Parameters:
    - network (list of tuples): The sorting network.
    - n (int): Number of inputs.
    
    Returns:
    - list: Mutated network.
    """
    new_network = network[:]
    if random.random() < 0.5 and len(new_network) > 0:
        new_network.pop(random.randint(0, len(new_network) - 1))
    else:
        i, j = random.sample(range(n), 2)
        new_network.append((min(i, j), max(i, j)))
    return new_network


def evolve_network(n, max_comparators, generations, population_size):
    """
    Evolve a sorting network using a genetic algorithm.
    
    Parameters:
    - n (int): Number of inputs.
    - max_comparators (int): Maximum number of comparators.
    - generations (int): Number of generations.
    - population_size (int): Size of the population.
    
    Returns:
    - list: The best evolved sorting network.
    """
    population = [generate_random_network(n, max_comparators) for _ in range(population_size)]
    for _ in range(generations):
        population.sort(key=lambda net: fitness(net, n), reverse=True)
        new_population = population[:population_size // 2]  # Keep the top half
        while len(new_population) < population_size:
            parent = random.choice(population[:population_size // 4])
            child = mutate(parent, n)
            new_population.append(child)
        population = new_population
    return population[0]


def plot_network(network, n):
    """
    Plot a sorting network as a graph with arrows indicating comparison-exchange steps.
    
    Parameters:
    - network (list of tuples): The sorting network.
    - n (int): Number of input lines (elements).
    """
    plt.figure(figsize=(14, 8))

    for i in range(n):
        plt.plot([0, len(network)], [i, i], color='black', linewidth=0.5)

    for step, (i, j) in enumerate(network):
        x = step + 1 
        plt.plot([x, x], [i, j], color='blue', linewidth=1.5)
        plt.scatter([x], [i], color='red', s=30)
        plt.scatter([x], [j], color='green', s=30) 

    plt.title("Sorting Network Visualization")
    plt.xlabel("Comparator Step")
    plt.ylabel("Input Lines")
    plt.xticks(range(0, len(network) + 1, 1))
    plt.yticks(range(0, n))
    plt.grid(axis='x', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    n = 16  
    max_comparators = 65 
    generations = 200 
    population_size = 50  

    evolved_network = evolve_network(n, max_comparators, generations, population_size)


    test_array = random.sample(range(100), n)
    print(f"Original array: {test_array}")
    sorted_array = apply_network(test_array[:], evolved_network)
    print(f"Sorted array: {sorted_array}")
    print(f"Number of comparators: {len(evolved_network)}")


    plot_network(evolved_network, n)
