import pygame as pg
import os

app_folder = os.path.dirname(os.path.dirname(__file__))


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, x, y) -> None:
        super().__init__()
        self.sprite_path = app_folder+"/resources/" + enemy_type + ".png"
        self.second_frame_path = app_folder+"/resources/" + enemy_type + "_b" + ".png"
        self.available_frames = [self.sprite_path, self.second_frame_path]

        self.image = pg.image.load(self.sprite_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.type_values = {
            "im2": 150,
            "im3": 200,
            "im4": 400
        }

        self.value: int = self.type_values[enemy_type]
        self.speed = 1

        self.right_dir = self.image
        self.left_dir = pg.transform.flip(self.image, True, False)

    def update(self, dir) -> None:
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

        self.rect.x += direction * self.speed


class BonusEnemy(pg.sprite.Sprite):
    def __init__(self, side, scr_w) -> None:
        super().__init__()
        self.image = pg.image.load(
            app_folder+"/resources/im1.png").convert_alpha()

        self.frame_one = app_folder+"/resources/im1.png"
        self.frame_two = app_folder+"/resources/im1_b.png"

        self.left_dir = self.image
        self.right_dir = pg.transform.flip(
            self.image, True, False)

        self.side = side
        if self.side == "right":
            x = scr_w + 45
            self.speed = -3
            self.image = self.right_dir
        else:
            x = - 45
            self.speed = 3
            self.image = self.left_dir

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self) -> None:
        self.rect.x += self.speed
