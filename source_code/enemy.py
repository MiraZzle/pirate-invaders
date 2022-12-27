import pygame as pg


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, x, y) -> None:
        super().__init__()
        self.sprite_path = "./resources/" + enemy_type + ".png"
        self.second_frame_path = "./resources/" + enemy_type + "_b" + ".png"

        self.available_frames = [self.sprite_path, self.second_frame_path]

        self.image = pg.image.load(self.sprite_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.type_values = {
            "im2": 150,
            "im3": 200,
            "im4": 400
        }

        self.current_time = 0
        self.value = self.type_values[enemy_type]
        self.current_frame = 0

        self.right_dir = self.image
        self.left_dir = pg.transform.flip(self.image, True, False)

    def update(self, dir) -> None:
        self.direction = dir
        self.handle_animation()
        self.move_x(dir)

    def handle_animation(self) -> None:
        self.current_time += 1
        if self.current_time % 20 == 0:
            self.current_time = 0
            self.current_frame += 1
            self.current_frame = self.current_frame % 2

            self.image = pg.image.load(
                self.available_frames[self.current_frame]).convert_alpha()
            self.right_dir = self.image
            self.left_dir = pg.transform.flip(self.image, True, False)

        if self.direction > 0:
            self.image = self.right_dir
        else:
            self.image = self.left_dir

    def move_x(self, direction) -> None:
        """"Moves enemy on x axis at directional speed"""
        self.rect.x += direction


class BonusEnemy(pg.sprite.Sprite):
    def __init__(self, side, scr_w) -> None:
        super().__init__()
        self.image = pg.image.load("./resources/im1.png").convert_alpha()

        self.frame_one = "./resources/im1.png"
        self.frame_two = "./resources/im1_b.png"

        self.current_time = 0
        self.current_frame = 0

        self.left_dir = self.image
        self.right_dir = pg.transform.flip(
            self.image, True, False)

        self.side = side
        if self.side == "right":
            x = scr_w + 50
            self.speed = -4
            self.image = self.right_dir
        else:
            x = - 50
            self.speed = 4
            self.image = self.left_dir

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self) -> None:
        self.rect.x += self.speed
        self.handle_animation()

    def handle_animation(self) -> None:
        self.available_frames = [self.frame_one, self.frame_two]

        self.current_time += 1
        if self.current_time % 20 == 0:
            self.current_time = 0
            self.current_frame += 1
            self.current_frame = self.current_frame % 2

            self.image = pg.image.load(
                self.available_frames[self.current_frame]).convert_alpha()

            self.right_dir = self.image
            self.left_dir = pg.transform.flip(self.image, True, False)

        if self.side == "right":
            self.image = self.left_dir
        else:
            self.image = self.right_dir
