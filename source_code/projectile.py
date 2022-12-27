import pygame as pg


class Projectile(pg.sprite.Sprite):
    def __init__(self, pos, texture, speed, scr_height) -> None:
        """Basic setup"""

        super().__init__()
        self.image = pg.image.load(texture)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.max_y = scr_height

    def queue_free(self) -> None:
        """Projectile is deleted if 30px above or under the screen"""

        if self.rect.y <= -30:
            self.kill()
        elif self.rect.y >= self.max_y + 30:
            self.kill()

    def update(self) -> None:
        """Moves projectile and checks for position"""

        self.rect.y -= self.speed
        self.queue_free()
