from heapq import heappop, heappush
import matplotlib.pyplot as plt


# Moves for a tile (Up, Down, Left, Right)
MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def manhattan_distance(state, goal):
    """Return the sum of the Manhattan distances of the tiles from their goal positions"""
    size = 3
    return sum(abs(i // size - g // size) + abs(i % size - g % size)
               for (i, g) in ((state.index(n), goal.index(n)) for n in range(1, size*size)))

def number_of_misplaced_tiles(state, goal):
    """Return the number of misplaced tiles"""
    return sum(s != g for (s, g) in zip(state, goal))

def find_neighbors(state):
    """Return the states reachable from state"""
    size = 3
    i = state.index(0)  # The position of the blank
    (x, y) = divmod(i, size)
    for (dx, dy) in MOVES:
        (nx, ny) = (x + dx, y + dy)
        if 0 <= nx < size and 0 <= ny < size:
            next_state = state.copy()
            next_state[i], next_state[nx * size + ny] = next_state[nx * size + ny], next_state[i]
            yield (1, next_state)

def reconstruct_path(seen, state):
    """Return the path from the start state to state"""
    return [] if state is None else reconstruct_path(seen, seen[tuple(state)]) + [state]

def solve_puzzle(start, heuristic):
    """Main function to solve the puzzle."""
    # Define the goal state
    goal = list(range(1, 9)) + [0]
    
    # Define the heuristic function
    if heuristic == 1:
        h = lambda s: 0  # Uniform Cost Search
    elif heuristic == 2:
        h = lambda s: number_of_misplaced_tiles(s, goal)
    elif heuristic == 3:
        h = lambda s: manhattan_distance(s, goal)

    # Priority queue, where the priority (score) is the first element
    queue = [(h(start), start)]

    # Dictionary of {state: predecessor}
    seen = {tuple(start): None}

    max_queue_size = 1  # Keep track of max queue size

    while queue:
        (priority, state) = heappop(queue)
        if state == goal:
            path = reconstruct_path(seen, state)
            solution_depth = len(path) - 1
            num_nodes_expanded = len(seen)
            solution_info = {
                'solution_depth': solution_depth,
                'num_nodes_expanded': num_nodes_expanded,
                'max_queue_size': max_queue_size,
            }
            return path, solution_info
        for (cost, next_state) in find_neighbors(state):
            if tuple(next_state) not in seen:
                priority = cost + h(next_state)
                heappush(queue, (priority, next_state))
                seen[tuple(next_state)] = state
                max_queue_size = max(max_queue_size, len(queue))  # Update max queue size if necessary
    return []



def input_puzzle():
    """Prompt the user to input the initial state of the puzzle and the heuristic to use"""
    puzzle_type = int(input("If you want to use default puzzle, please enter 1, if you want to set the puzzle by yourself, please input 2 :"))
    if puzzle_type == 1:
        difficulty_type = int(input("The preset puzzle has 8 different levels of difficulty, enter 1 to 8 to select one of the levels:"))
        if difficulty_type == 1:
            start = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        elif difficulty_type == 2:
            start = [1, 2, 3, 4, 5, 6, 0, 7, 8]
        elif difficulty_type == 3:
            start = [1, 2, 3, 5, 0, 6, 4, 7, 8]
        elif difficulty_type == 4:
            start = [1, 3, 6, 5, 0, 2, 4, 7, 8]
        elif difficulty_type == 5:
            start = [1, 3, 6, 5, 0, 7, 4, 8, 2]
        elif difficulty_type == 6:
            start = [1, 6, 7, 5, 0, 3, 4, 8, 2]
        elif difficulty_type == 7:
            start = [7, 1, 2, 4, 8, 5, 6, 3, 0]
        elif difficulty_type == 8:
            start = [0, 7, 2, 4, 6, 1, 3, 5, 8]
        else:
            print("Please enter 1 to 8 to select one of the levels.")
            return input_puzzle()
    else:
        print("Please enter the initial state of the puzzle, 0 for empty space, and enter 9 numbers separated by spaces.")
        start = list(map(int, input().split()))
    heuristic = int(input("Please select the heuristic function (input 1 for UCS, 2 for misplaced, 3 for manhattan):"))
    return start, heuristic


def print_state(state):
    """Print the state of the puzzle"""
    size = 3
    for i in range(size):
        for j in range(size):
            print(state[i*size + j], end=" ")
        print()
    print()  # This will print an empty line after each state

def collect_results(start):
    """Collect results for all heuristics and plot them."""
    results = {}
    metrics = ['solution_depth', 'num_nodes_expanded', 'max_queue_size']
    for heuristic in [1, 2, 3]:  # Iterate over all heuristics
        _, results[heuristic] = solve_puzzle(start, heuristic)

    # Prepare data for plotting
    data_to_plot = {metric: [] for metric in metrics}
    for heuristic, result in results.items():
        for metric in metrics:
            data_to_plot[metric].append(result[metric])

    # Plot the results
    for metric, data in data_to_plot.items():
        plt.figure()
        plt.bar(['UCS', 'Misplaced Tiles', 'Manhattan Distance'], data)
        plt.title('Comparison of Heuristics by {}'.format(metric))
        plt.ylabel(metric)
        plt.show()


def main(): 
    start, heuristic = input_puzzle()
    path, solution_info = solve_puzzle(start, heuristic)
    if path:
        print("Puzzle has solved!")
        for state in path:
            print_state(state)

        print(f"Solution depth: {solution_info['solution_depth']}")
        print(f"Number of nodes expanded: {solution_info['num_nodes_expanded']}")
        print(f"Max queue size: {solution_info['max_queue_size']}")
    else:
        print("Fail to solve.")
        
    collect_results(start)


main()