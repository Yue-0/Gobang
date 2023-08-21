from typing import Union
from random import choice

import numpy as np

from game import Gobang, BLACK, WHITE


class MiniMaxSearch:
    """
    Minimax search algorithm using alpha-beta pruning
    """
    def __init__(self, depth: int, breadth: int = 0):
        """
        :param depth: Maximum search depth.
        :param breadth: Maximum search breadth.
                        If set to 0, the breadth will be unlimited. Default: 0.
        """
        n, p = sorted([BLACK, WHITE])
        sleep2 = [(p, 0, 0, 0, p),
                  (n, p, p, 0, 0, 0),
                  (n, p, 0, p, 0, 0),
                  (n, p, 0, 0, p, 0)]
        alive2 = [(p, 0, 0, p),
                  (0, p, 0, p, 0),
                  (0, 0, p, p, 0, 0)]
        sleep3 = [(p, p, 0, 0, p),
                  (p, 0, p, 0, p),
                  (n, p, p, p, 0, 0),
                  (n, p, p, 0, p, 0),
                  (n, p, 0, p, p, 0)]
        alive3 = [(0, p, p, p, 0),
                  (0, p, p, 0, p, 0)]
        sleep4 = [(p, p, p, 0, p),
                  (p, p, 0, p, p),
                  (n, p, p, p, p, 0)]
        alive4 = [(0, p, p, p, p, 0)]
        for samples in (sleep2, sleep3, sleep4, alive2, alive3, alive4):
            for sample in samples:
                reverse = sample[::-1]
                if reverse not in samples:
                    samples.append(reverse)
        self.scores = {}
        score = {"sleep2": 1, "sleep3": 50, "sleep4": 500,
                 "alive2": 5, "alive3": 500, "alive4": 10000}
        for samples in score.keys():
            for sample in eval(samples):
                self.scores[sample] = score[samples]
        self.depth = depth << 1
        self.breadth = breadth

    def __call__(self, game: Gobang) -> tuple[int, int]:
        """
        :param game: Current chess game.
        :return: The best position for the next step.
        """
        step = game.step
        if step > 1:
            return self.search(game)
        if step == 1:
            x, y = game.history[0]
            x += choice([-1, 1])
            y += choice([-1, 1])
            return max(min(x, game.size), 0), max(min(y, game.size), 0)
        return game.size >> 1, game.size >> 1

    def score(self, game: Gobang) -> int:
        """
        Calculate the score of the game.
        """
        def part_score(array):
            s = 0
            if np.array(np.where(array)).shape[1] < 2:
                return s
            for sgn in (-1, 1):
                arr = sgn * array
                for i in range(game.size - 3):
                    for length in (4, 5, 6):
                        if i + length >= array.shape[0]:
                            break
                        p = arr[i: i + length]
                        if np.array(np.where(p)).shape[1] < 2:
                            continue
                        p = tuple(p)
                        if p in self.scores:
                            s += sgn * self.scores[p]
            return s

        score = 0
        for b in range(game.size):
            for part in (game.checkerboard[b, :], game.checkerboard[:, b]):
                score += part_score(part)
        for b in range(4 - game.size, game.size - 3):
            for part in (
                    [game.checkerboard[i, b + i] for i in range
                     (max(0, -b), min(game.size, game.size - b))],
                    [game.checkerboard[i, b + game.size - i - 1] for
                     i in range(max(0, b), min(game.size, game.size + b))]
            ):
                score += part_score(np.array(part))
        return score

    def expand(self, game: Gobang) -> list:
        """
        Return the extensions of the game.
        """
        if not self.breadth:
            return game.empty
        neighbors = set()
        for x0, y0 in game.history[::-1]:
            for x in range(
                    max(0, x0 - self.breadth),
                    min(game.size, x0 + self.breadth + 1)
            ):
                for y in range(
                        max(0, y0 - self.breadth),
                        min(game.size, y0 + self.breadth + 1)
                ):
                    if not game.checkerboard[x, y]:
                        neighbors.add((x, y))
        return list(neighbors)

    def search(self,
               game: Gobang,
               depth: int = 0,
               alpha: float = -float("inf"),
               beta: float = float("inf")) -> Union[tuple, float]:
        """
        :param game: Current chess game.
        :param depth: Current search depth. Default: 0.
        :param alpha: Current alpha value. Default: Negative infinity.
        :param beta: Current beta value. Default: Positive infinity.
        :return: If depth == 0, return the best placement position.
                 Otherwise, return the score of game.
        """
        if depth == self.depth:
            return self.score(game)
        color, result = game.next, []
        value = -np.sign(color) * np.inf
        for x, y in self.expand(game):
            copy = game.copy()
            if copy.play(x, y, color):
                value, result = np.sign(color) * np.inf, [(x, y)]
                break
            v = self.search(copy, depth + 1, alpha, beta)
            if color < 0:
                if depth:
                    value = min(value, v)
                elif value == v:
                    result.append((x, y))
                elif value > v:
                    value, result = v, [(x, y)]
                beta = min(beta, value)
            else:
                if depth:
                    value = max(value, v)
                elif value == v:
                    result.append((x, y))
                elif value < v:
                    value, result = v, [(x, y)]
                alpha = max(alpha, value)
            if alpha > beta:
                break
        return value if depth else choice(result)
