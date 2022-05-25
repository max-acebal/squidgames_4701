import numpy as np
import random
import time
import sys
import os
from Grid import Grid
from BaseAI import BaseAI
from Utils import basic_heuristic, move, utility,manhattan_distance

# TO BE IMPLEMENTED
#
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None

    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        # locate opponent cell
        available_moves = grid.get_neighbors(self.pos, only_available=True)
        if len(available_moves) > 0:
            best_move = self.move_max(self.pos, self.player_num, grid, 0, -100, 100)
            return best_move[0]
        else:
            return tuple("We Lost", "Rip")

    def move_max(self, pos, player_num, grid: Grid, depth, alpha, beta) -> tuple:
        available_moves = grid.get_neighbors(pos, only_available=True)
        if len(available_moves) == 0 or depth >= 5:
            return [pos, utility(player_num, 3 - player_num, grid)]

        best_move = [(-1, -1), (-100)]

        for child in available_moves:
            # throw trap into grid
            copy = grid.clone()
            copy.move(child, player_num)

            # minimize over opponent's possible moves
            check = self.move_min(child, player_num, copy, depth + 1, alpha, beta)

            if check[1] > best_move[1]:
                best_move[0] = child
                best_move[1] = check[1]

            alpha = max(alpha, best_move[1])

            if beta <= alpha:
                break

        return best_move

    def move_min(self, pos, player_num, grid: Grid, depth, alpha, beta) -> tuple:
        available_moves = grid.get_neighbors(pos, only_available=True)
        if len(available_moves) == 0 or depth >= 5:
            return [pos, utility(player_num, 3 - player_num, grid)]

        best_move = [(-1, -1), 100]

        for child in available_moves:
            # Sample an opponent move
            copy = grid.clone()
            copy.trap(child)

            probability = 1 - 0.05 * (manhattan_distance(child, self.pos) - 1)

            # maximize over possible trap spots
            check = self.move_max(pos, player_num, copy, depth + 1, alpha, beta)

            check[1] = check[1] * probability

            if check[1] < best_move[1]:
                best_move[0] = child
                best_move[1] = check[1]

            beta = min(beta, best_move[1])

            if beta <= alpha:
                break

        return best_move

    def getTrap(self, grid: Grid) -> tuple:
        # locate opponent cell
        opponent = grid.find(3 - self.player_num)

        available_moves = grid.get_neighbors(self.pos, only_available=True)
        if len(available_moves) > 0:
            best_trap = self.trap_max(opponent, grid, 0, -100, 100)
            if (grid.getCellValue(best_trap[0]) > 0):
              result = tuple(np.argwhere(grid.map == 0)[0])
              return result
            else:
              return best_trap[0]
        else:
            return tuple("We Lost", "Rip")

    def trap_max(self, opponent, grid, depth, alpha, beta):
        available_moves = grid.get_neighbors(opponent, only_available=True)
        if len(available_moves) == 0 or depth >= 5:
            return [opponent, utility(self.player_num, 3 - self.player_num, grid)]

        best_move = [(-1, -1), (-100)]

        for child in available_moves:
            # throw trap into grid
            copy = grid.clone()
            copy.trap(child)

            probability = 1 - 0.05 * (manhattan_distance(child, self.pos) - 1)

            # minimize over opponent's possible moves
            check = self.trap_min(opponent, copy, depth + 1, alpha, beta)
            check[1] = check[1] * probability

            if check[1] > best_move[1]:
                best_move[0] = child
                best_move[1] = check[1]

            alpha = max(alpha, best_move[1])

            if beta <= alpha:
                break

        return best_move

    def trap_min(self, opponent, grid, depth, alpha, beta):
        available_moves = grid.get_neighbors(opponent, only_available=True)
        if len(available_moves) == 0 or depth >= 5:
            return [opponent, utility(self.player_num, 3 - self.player_num, grid)]

        best_move = [(-1, -1), 100]

        for child in available_moves:
            # Sample an opponent move
            copy = grid.clone()
            copy.move(child, 3 - self.player_num)

            # maximize over possible trap spots
            check = self.trap_max(opponent, copy, depth + 1, alpha, beta)

            if check[1] < best_move[1]:
                best_move[0] = child
                best_move[1] = check[1]

            beta = min(beta, best_move[1])

            if beta <= alpha:
                break

        return best_move
