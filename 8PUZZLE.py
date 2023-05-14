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