import pygame as pg


class Wall(pg.sprite.Sprite):
    def __init__(self, size, color, x, y) -> None:
        """Creates square piece of wall"""

        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


# Shape of wall, may be altered in any way, "X" represents placed cells
shape = [
    "XXXXXXXXXXX",
    "XXXXXXXXXXX",
    "XXXXXXXXXXX",
    "XX       XX",
    "XX       XX",
    "XX       XX"
]
