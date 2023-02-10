import pygame as pg

import game
from AI import AI

SMALL, MEDIUM, LARGE = tuple(range(3))  # Used to represent font size
EXIT, CHOOSE, PLAY, OVER = tuple(range(4))  # Used to indicate program status


class GameInterface:
    def __init__(self,
                 name: str,
                 game_size: int = 15,
                 interface_size: tuple[int, int] = (1195, 795),
                 background: tuple[int, int, int] = (250, 218, 141)):
        """
        :param name: Name of interface.
        :param game_size: The size of the game board. Default: 15.
        :param interface_size: Width and height of game interface.
                               Default: (1195, 795).
        :param background: Background RGB color of game interface.
                           Default: (250, 218, 141).
        """
        pg.init()
        self.ai = AI()
        self.win = None
        self.run = CHOOSE
        self.size = interface_size
        pg.display.set_caption(name)
        self.game = game.Gobang(game_size)
        self.player = {game.BLACK: "", game.WHITE: ""}
        pg.display.set_icon(pg.image.load("icon.jpeg"))
        self.interface = pg.display.set_mode(self.size)
        tian_yuan, star = game_size >> 1, game_size >> 2
        self.stars = (
            (star, star),
            (tian_yuan, tian_yuan),
            (star, self.game.size - star - 1),
            (self.game.size - star - 1, star),
            (self.game.size - star - 1, self.game.size - star - 1)
        )
        self.fonts = [pg.font.Font("font.ttf", self.size[1] // k)
                      for k in range(25, 10, -5)]
        self.colors = {
            "BG": background,
            "RED": (255, 0, 0),
            "GRAY": (127,) * 3,
            "WHITE": (255,) * 3,
            "BLACK": (0, 0, 0),
            "GREEN": (0, 255, 0)
        }
        for color in ("BLACK", "WHITE"):
            self.colors[str(eval(f"game.{color}"))] = self.colors[color]
        self.down = 7 * (self.size[1] >> 3)
        self.left = (self.size[0] - self.size[1]) >> 1
        self.size0 = self.size[1] // (self.game.size << 1)
        self.right = self.left + 2 * (self.game.size - 1) * self.size0
        self.radius, self.thickness = self.size[1] // 40, self.size[1] // 200
        self.restart()

    @property
    def now(self) -> int:
        """
        :return: Players who currently need to play.
        """
        return self.game.next

    @property
    def ready(self) -> bool:
        """
        :return: Whether the game can start.
        """
        ready = False
        for player in self.player.values():
            if player == "":
                return False
            if player == "Human":
                ready = True
        return ready

    @property
    def repent(self) -> bool:
        """
        :return: Whether the current player can repent.
        """
        if self.run != PLAY:
            return False
        if self.player[game.BLACK] == "Human":
            return bool(self.game.step)
        else:
            return self.game.step > 1

    def show(self) -> None:
        """
        Start display interface
        """
        while self.run:
            self.loop()

    def loop(self) -> None:
        """
        Program main loop.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.run = EXIT
                break
            if self.run == CHOOSE and event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                d = self.size[1] >> 3
                if x < self.left:
                    if 3 * d < y < 4 * d:
                        if self.player[game.BLACK] == "AI":
                            self.player[game.BLACK] = ""
                        else:
                            self.player[game.BLACK] = "AI"
                    elif 6 * d < y < 7 * d:
                        if self.player[game.WHITE] == "AI":
                            self.player[game.WHITE] = ""
                        else:
                            self.player[game.WHITE] = "AI"
                    elif 2 * d < y < 3 * d:
                        if self.player[game.BLACK] == "Human":
                            self.player[game.BLACK] = ""
                        else:
                            self.player[game.BLACK] = "Human"
                    elif 5 * d < y < 6 * d:
                        if self.player[game.WHITE] == "Human":
                            self.player[game.WHITE] = ""
                        else:
                            self.player[game.WHITE] = "Human"
                elif x > self.right and y > 7 * d and self.ready:
                    self.run = PLAY
                self.update()
                break
            elif self.run == PLAY:
                if self.player[self.now] == "AI":
                    self.wait()
                    self.play(*self.ai(self.game.copy()))
                    break
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.left - self.size0 < x < self.right + self.size0:
                        try:
                            self.play(*self.get_click(x, y))
                        except AssertionError:
                            pass
                        break
                    if x > self.right and y > self.down:
                        self.restart()
                        break
                    if self.repent and x < self.left and y > self.down:
                        self.revoke()
                        break
            elif self.run == OVER and event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x > self.right and y > self.down:
                    self.restart()
                    break

    def play(self, x: int, y: int) -> None:
        """
        Drop the pawn at (x, y).
        """
        assert not self.game.checkerboard[x, y]
        if self.game.step:
            px, py = self.transform(*self.game.history[-1])
            self.draw_circle(px, py, self.radius, str(-self.now))
        over = self.game.play(x, y, self.now)
        x, y = self.transform(x, y)
        if over or self.game.full:
            self.run = OVER
            if over:
                self.win = -self.now
        self.draw_circle(x, y, self.radius, str(-self.now))
        self.draw_circle(x, y, self.thickness, "RED")
        self.update()

    def wait(self) -> None:
        """
        Waiting for AI decision.
        """
        self.put_text(
            self.right + self.size[0] // 60,
            self.size[1] >> 1, "AI is thinking", "BLACK", SMALL
        )
        pg.display.update()

    def erase(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Erase the contents of rectangular region (x1, y1, x2, y2).
        """
        pg.draw.rect(self.interface, self.colors["BG"], (x1, y1, x2, y2))

    def revoke(self) -> None:
        """
        Current player repents once.
        """
        last = self.game.revoke()
        x, y = self.transform(*last)
        self.draw_circle(x, y, self.radius, "BG")
        self.draw_line(x - self.radius, y, x + self.radius, y)
        self.draw_line(x, y - self.radius, x, y + self.radius)
        if last in self.stars:
            self.draw_circle(
                self.left + 2 * self.size0 * last[0],
                (2 * last[1] + 1) * self.size0,
                self.thickness << 1,
                "BLACK"
            )
        if self.player[self.now] == "AI":
            self.revoke()
        elif self.game.step:
            self.play(*self.game.revoke())
        else:
            self.update()

    def update(self) -> None:
        """
        Update game interface.
        """
        if self.run == CHOOSE:
            y, d = [self.size[1] >> 3] * 2
            self.erase(0, 0, self.left - self.thickness, self.size[1])
            for color in ("Black", "White"):
                self.put_text(self.radius, y, color, "BLACK", LARGE)
                color = eval(f"game.{color.upper()}")
                for player in ("Human", "AI"):
                    y += d
                    self.put_text(
                        self.radius, y, f"· {player}", font=MEDIUM,
                        color="RED" if player == self.player[color] else "GRAY"
                    )
                y += d
            self.put_text(
                self.right + self.radius, self.down,
                "Play", "GREEN" if self.ready else "GRAY", MEDIUM
            )
        else:
            self.erase(
                self.right + self.radius,
                self.size[1] >> 1,
                self.size[0],
                self.size[1]
            )
            self.put_text(
                self.right + self.radius,
                self.down, "Restart", "GREEN", MEDIUM
            )
            if self.repent:
                self.put_text(self.radius, self.down, "Repent", "GREEN", MEDIUM)
            else:
                self.erase(
                    0, self.down, self.left - self.thickness, self.size[1]
                )
            if self.run == OVER:
                winner = "Tie" if self.win is None else "Winner: {}".format(
                    "Black" if self.win == game.BLACK else "White"
                )
                self.put_text(
                    self.right + self.radius,
                    self.size[1] >> 1, winner, "BLACK", SMALL
                )
        pg.display.update()

    def restart(self) -> None:
        """
        Restart the game.
        """
        self.win = None
        self.run = CHOOSE
        self.game.restart()
        self.interface.fill(self.colors["BG"])
        y = (2 * self.game.size - 1) * self.size0
        for line in range(1, self.game.size << 1, 2):
            line *= self.size0
            x = self.left - self.size0 + line
            self.draw_line(x, self.size0, x, y)
            self.draw_line(self.left, line, self.right, line)
        for x, y in self.stars:
            self.draw_circle(
                self.left + 2 * self.size0 * x,
                (2 * y + 1) * self.size0,
                self.thickness << 1,
                "BLACK"
            )
        self.update()

    def transform(self, x: int, y: int) -> tuple[int, int]:
        """
        Convert game coordinates (x, y) to interface coordinates.
        """
        return self.left + 2 * x * self.size0, (2 * y + 1) * self.size0

    def put_text(self, x: int, y: int, text: str, color: str, font: int) -> \
            None:
        """
        Display text on the interface.
        :param x: The x-coordinate of the upper-left corner of the text.
        :param y: The y-coordinate of the upper-left corner of the text.
        :param text: Text content.
        :param color: Color of text.
        :param font: Font size, can be SMALL, MEDIUM or LARGE.
        """
        self.interface.blit(self.fonts[font].render(text, True, color), (x, y))

    def get_click(self, x: int, y: int) -> tuple[int, int]:
        """
        Convert interface coordinates (x, y) to game coordinates.
        """
        x = max(0, x - self.left) // self.size0 + 1
        y = max(0, y - self.size0) // self.size0 + 1
        return x >> 1, y >> 1

    def draw_line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Draw a line from (x1, y1) to (x2, y2).
        """
        pg.draw.line(
            self.interface,
            self.colors["BLACK"],
            (x1, y1), (x2, y2),
            self.thickness
        )

    def draw_circle(self, x: int, y: int, r: int, color: str) -> None:
        """
        Draw a circle.
        :param x: Circle center's x-coordinate.
        :param y: Circle center's y-coordinate.
        :param r: Radius of circle.
        :param color: Color of circle.
        """
        pg.draw.circle(self.interface, self.colors[color], (x, y), r)


if __name__ == "__main__":
    GameInterface("Gobang", 15).show()
