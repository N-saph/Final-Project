import matplotlib.pyplot as plt
import random

def apply_sorting_network(arr, network):
    """
    Apply a sorting network to an array.

    Parameters:
    - arr (list): The array to sort.
    - network (list of tuples): The sorting network (comparators).

    Returns:
    - list: The sorted array.
    """
    for (i, j) in network:
        if arr[i] > arr[j]:
            arr[i], arr[j] = arr[j], arr[i]
    return arr


def batcher_sort(n):
    """
    Generate Batcher's sorting network for n elements.
    This function works for sizes that are powers of two or near powers of two.

    Parameters:
    - n (int): Number of elements to sort.

    Returns:
    - list: A list of tuples, where each tuple is a comparator (i, j).
    """
    def merge(lo, n, step):
        """Merge subarrays in Batcher's odd-even mergesort."""
        if n > 1:
            mid = n // 2
            merge(lo, mid, step * 2)
            merge(lo + step, mid, step * 2)
            odd_even_merge(lo, n, step)

    def odd_even_merge(lo, n, step):
        """Odd-even merging stage."""
        step *= 2
        if step < n:
            odd_even_merge(lo, n, step)
            odd_even_merge(lo + step, n, step)
            for i in range(lo + step, lo + n - step, step * 2):
                comparators.append((i, i + step))
        else:
            for i in range(lo, lo + n - step, step):
                comparators.append((i, i + step))

    comparators = []
    merge(0, n, 1)
    return comparators


def optimal_16_input_sorting_network():
    """
    Return the optimal 16-input sorting network with 60 comparators.

    Returns:
    - list: A list of tuples, where each tuple is a comparator (i, j).
    """
    return [
        (0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15),
        (0, 2), (1, 3), (4, 6), (5, 7), (8, 10), (9, 11), (12, 14), (13, 15),
        (0, 4), (1, 5), (2, 6), (3, 7), (8, 12), (9, 13), (10, 14), (11, 15),
        (0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13), (6, 14), (7, 15),
        (5, 10), (6, 9), (3, 12), (13, 14),
        (1, 2), (4, 8), (11, 13), (7, 15),
        (2, 8), (5, 9), (6, 10), (3, 12),
        (1, 4), (7, 13), (11, 14), (9, 12),
        (1, 3), (2, 5), (6, 9), (10, 12),
        (3, 7), (2, 4), (6, 8), (10, 13),
    ]


def plot_network(network, n):
    """
    Plots the sorting network as a graph with horizontal and vertical lines.

    Parameters:
    - network (list of tuples): The sorting network, where each tuple (i, j) is a comparator.
    - n (int): Number of input lines (elements).
    """
    plt.figure(figsize=(12, 8))
    
    for i in range(n):
        plt.plot([0, len(network)], [i, i], color='black', linewidth=0.5)

    for step, (i, j) in enumerate(network):
        x = step + 1
        plt.plot([x, x], [i, j], color='green', linewidth=1.5)
        plt.scatter([x, x], [i, j], color='red', s=10)

    plt.title("Sorting Network Visualization")
    plt.xlabel("Comparator Step")
    plt.ylabel("Input Lines")
    plt.xticks(range(0, len(network) + 1, 1))
    plt.yticks(range(0, n))
    plt.grid(axis='x', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


def test_network():
    n = 16
    input_array = list(range(n))
    shuffled_array = input_array[:]
    random.shuffle(shuffled_array)

    print(f"Original array: {shuffled_array}")

    batcher_network = batcher_sort(n)
    batcher_sorted = apply_sorting_network(shuffled_array[:], batcher_network)
    print(f"Batcher's sorted array: {batcher_sorted}")
    print(f"Batcher's network comparators: {len(batcher_network)}")
    plot_network(batcher_network, n)

    optimal_network = optimal_16_input_sorting_network()
    optimal_sorted = apply_sorting_network(shuffled_array[:], optimal_network)
    print(f"Optimal sorted array: {optimal_sorted}")
    print(f"Optimal network comparators: {len(optimal_network)}")
    plot_network(optimal_network, n)


test_network()

