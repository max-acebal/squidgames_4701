import numpy as np
from Grid import Grid


def manhattan_distance(position, target):
    return np.abs(target[0] - position[0]) + np.abs(target[1] - position[1])


def basic_heuristic(location, grid: Grid) -> int:
    return move(grid.get_neighbors(location, only_available=True), grid)


def utility(player1, player2, grid):
    loc_1 = grid.find(player1)
    centerdict = {
        (3, 3): 0.3,
        (3, 2): 0.2,
        (2, 3): 0.2,
        (3, 4): 0.2,
        (4, 3): 0.2
    }
    center_util = 0
    corner_util = 0

    if centerdict.get(loc_1) is not None:
        center_util += centerdict.get(loc_1)

    if loc_1[0] == 0 or loc_1[0] == 6:
        corner_util -= 0.4
    if loc_1[1] == 0 or loc_1[1] == 6:
        corner_util -= 0.4

    return corner_util + center_util + len(grid.get_neighbors(grid.find(player1), only_available=True)) - len(
        grid.get_neighbors(grid.find(player2), only_available=True))


def move(available_moves, grid: Grid) -> int:
    max_neighbors = 0
    new_pos = available_moves[0]
    for option in available_moves:
        current_size = len(grid.get_neighbors(option, only_available=True))
        if current_size > max_neighbors:
            max_neighbors = current_size
            new_pos = option
    return new_pos
