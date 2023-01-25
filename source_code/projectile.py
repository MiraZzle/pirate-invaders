"""Projectile module in main game. Handles projectile movement and destruction."""

import pygame as pg


class Projectile(pg.sprite.Sprite):
    def __init__(self, pos, texture, speed, scr_height) -> None:
        """Basic setup"""

        super().__init__()
        self.image = pg.image.load(texture)  # loads projectile image
        # collision object with image size, pos set to midbottom of image
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.max_y = scr_height  #  used for projectile kill threshold position

    def queue_free(self) -> None:
        """Projectile is deleted if is out of the screen"""

        if self.rect.y <= -30:
            self.kill()  #  removes sprite from all groups, makes it unresponsive and stops drawing
        elif self.rect.y >= self.max_y + 30:
            self.kill()  #  removes sprite from all groups, makes it unresponsive and stops drawing

    def update(self) -> None:
        """Moves projectile and checks for position"""

        self.rect.y -= self.speed
        self.queue_free()
