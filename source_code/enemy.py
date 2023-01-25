"""Handles enemies."""

import pygame as pg
import os

# parent directory of current file parent directory
app_folder = os.path.dirname(os.path.dirname(__file__))

"""Enemy module in main game. Handles enemy movement."""


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, x, y) -> None:
        """Init"""

        super().__init__()
        self.sprite_path = app_folder+"/resources/" + \
            enemy_type + ".png"  # assigns path to image according to value in enemy_type

        self.image = pg.image.load(
            self.sprite_path).convert_alpha()         # loads enemy image
        # collision object with image size, topleft pos set to passed coords
        self.rect = self.image.get_rect(topleft=(x, y))

        # dictionary for points assigned for destroying enemy by type
        self.type_values = {
            "im2": 150,
            "im3": 200,
            "im4": 400
        }

        #  set current enemy value
        self.value: int = self.type_values[enemy_type]
        self.speed = 1

        self.right_dir = self.image
        #  flip enemy image horizontally
        self.left_dir = pg.transform.flip(self.image, True, False)

    def update(self, dir) -> None:
        """Updates enemy"""
        self.direction = dir
        self.handle_sprite()
        self.move_x(dir)

    def handle_sprite(self) -> None:
        """Handles animation, every 20 ticks new frame is set, animation speed = 3 FPS"""

        if self.direction > 0:
            self.image = self.right_dir
        else:
            self.image = self.left_dir

    def move_x(self, direction) -> None:
        """"Moves enemy on x axis at directional speed"""

        self.rect.x += direction * self.speed  #  changes rect object position on x axis


"""Bonus enemy module in main game. Handles enemy movement."""


class BonusEnemy(pg.sprite.Sprite):
    def __init__(self, side, scr_w) -> None:
        """Init"""
        super().__init__()
        self.image = pg.image.load(
            app_folder+"/resources/im1.png").convert_alpha()  # loads enemy image, convert_to_alpha() changes image pixel format according to screen

        self.frame_one = app_folder+"/resources/im1.png"
        self.frame_two = app_folder+"/resources/im1_b.png"

        self.left_dir = self.image
        self.right_dir = pg.transform.flip(
            self.image, True, False)  #  flip enemy image horizontally

        self.side = side
        if self.side == "right":  #  if enemy spawns on right side
            x = scr_w + 45
            self.speed = -3
            self.image = self.right_dir
        else:  #  enemy spawns on left
            x = - 45
            self.speed = 3
            self.image = self.left_dir

        #  collision object with image size, topleft pos set to passed x coord, 80 pixels from top
        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self) -> None:
        self.rect.x += self.speed
