from heapq import heappop, heappush

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

def solve_puzzle(start, heuristic=1):
    size = 3
    # Define the goal state
    goal = list(range(1, size*size)) + [0]
    
    # Define the heuristic function
    if heuristic == 3:  # Manhattan
        h = manhattan_distance
    elif heuristic == 2:  # Misplaced
        h = number_of_misplaced_tiles
    else:  # UCS
        h = lambda state, goal: 0

    # Priority queue, where the priority (score) is the first element
    queue = [(h(start, goal), start)]

    # Dictionary of {state: predecessor}
    seen = {tuple(start): None}

    while queue:
        (priority, state) = heappop(queue)
        if state == goal:
            return reconstruct_path(seen, state)
        for (cost, next_state) in find_neighbors(state):
            if tuple(next_state) not in seen:
                priority = cost + h(next_state, goal)
                heappush(queue, (priority, next_state))
                seen[tuple(next_state)] = state
    return []