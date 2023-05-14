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