import numpy as np

__all__ = ["BLACK", "WHITE", "Gobang"]

BLACK, WHITE = 1, -1
assert BLACK + WHITE == 0, "BLACK and WHITE must be opposite numbers"


class Gobang:
    def __init__(self, size: int, connection: int = 5):
        """
        :param size: The size of the chessboard will be size x size.
        :param connection: Number of consecutive pieces required for victory.
                           Default: 5.
        """
        self.size = size
        self.history = []
        self.connection = connection
        self.checkerboard = np.zeros((size, size), np.int8)

    def __eq__(self, other):
        if isinstance(other, Gobang):
            return self.checkerboard.tolist() == other.checkerboard.tolist()
        return False

    def __str__(self):
        return "\n".join([
            " ".join(map(str, line)).replace("-1", "W").replace("1", "B")
            for line in self.checkerboard // BLACK
        ])

    def __hash__(self):
        return hash(int("".join(map(
            str, self.checkerboard.flatten() // BLACK
        )).replace("-1", "2"), 3))

    @property
    def step(self) -> int:
        """
        :return: The number of pieces currently on the board.
        """
        return len(self.history)

    @property
    def full(self) -> bool:
        """
        :return: Whether the current checkerboard is full.
        """
        return self.step == self.size ** 2

    @property
    def next(self) -> int:
        """
        :return: The color of the current player.
        """
        return WHITE if self.step % 2 else BLACK

    @property
    def empty(self) -> list:
        """
        :return: A list of all empty coordinates on the checkerboard.
        """
        return np.array(np.where(self.checkerboard == 0)).T.tolist()

    def win(self, x: int, y: int) -> bool:
        """
        :return: If piece (x, y) wins the game then return True.
        """
        def win(x0, y0, f, g):
            color, connection = self.checkerboard[x0, y0], 1
            if not color:
                return False
            for sign in (-1, 1):
                for bias in range(sign, sign * self.connection, sign):
                    i, j = f(x0, bias), g(y0, bias)
                    if self.legal(i, j) and self.checkerboard[i, j] == color:
                        connection += 1
                    else:
                        break
                    if connection == self.connection:
                        return True
            return False

        return (win(x, y, lambda z, b: z + b, lambda z, b: z - b) or
                win(x, y, lambda z, b: z + b, lambda z, b: z + b) or
                win(x, y, lambda z, b: z + b, lambda z, b: y) or
                win(x, y, lambda z, b: x, lambda z, b: z + b))

    def copy(self):
        """
        :return: A copy of the current object.
        """
        copy = Gobang(self.size, self.connection)
        copy.update(self.checkerboard, self.history)
        return copy

    def play(self, x: int, y: int, color: int = 0) -> bool:
        """
        Drop the pawn of color at (x, y).
        If color == 0 (default), color will be judged automatically.
        :return: Victory or not.
        """
        assert not self.checkerboard[x, y]
        if not color:
            color = self.next
        self.checkerboard[x, y] = color
        self.history.append([x, y])
        return self.win(x, y)

    def legal(self, x: int, y: int) -> bool:
        """
        :return: Whether coordinate (x, y) is inside the chessboard.
        """
        return 0 <= min(x, y) and max(x, y) < self.size

    def revoke(self) -> tuple[int, int]:
        """
        Undo the last action.
        :return: Coordinate of the last action.
        """
        x, y = self.history.pop()
        self.checkerboard[x, y] = 0
        return x, y

    def update(self, checkerboard: np.ndarray, history: list = None) -> None:
        """
        Set checkerboard and historical chess game.
        :param checkerboard: Checkerboard content.
        :param history: Historical chess game.
                        If None, it will be automatically generated.
                        Default: None.
        """
        if history is None:
            history = []
            black, white = [np.where(self.checkerboard == color).T.tolist()
                            for color in (BLACK, WHITE)]
            while white:
                history.append(black.pop())
                history.append(white.pop())
            history += black
        self.history = [c for c in history]
        self.checkerboard = checkerboard.astype(np.int8)

    def restart(self) -> None:
        """
        Restart the game.
        """
        self.history.clear()
        self.checkerboard *= 0
