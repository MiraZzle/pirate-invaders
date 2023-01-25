"""Wall module in main game."""

import pygame as pg


class Wall(pg.sprite.Sprite):
    def __init__(self, size, color, x, y) -> None:
        """Creates square piece of wall"""

        super().__init__()
        # creates image object of given width (= size) and length (= size)
        self.image = pg.Surface((size, size))
        self.image.fill(color)  # fills image object with given color
        # collision object with image size, topleft pos set to passed coords
        self.rect = self.image.get_rect(topleft=(x, y))


# Shape of wall may be altered in any way, "X" represents placed blocks / cells
shape = [
    "XXXXXXXXXXX",
    "XXXXXXXXXXX",
    "XXXXXXXXXXX",
    "XX       XX",
    "XX       XX",
    "XX       XX"
]
