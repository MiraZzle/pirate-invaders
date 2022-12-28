import pygame as pg
from projectile import Projectile


class Player(pg.sprite.Sprite):
    def __init__(self, pos, scr_w, speed) -> None:
        """Init"""

        super().__init__()
        self.image = pg.image.load(
            "./resources/im5.png").convert_alpha()

        self.sprite_path = "./resources/im5.png"  # Path to first frame of anim
        self.second_frame_path = "./resources/im5_b.png"  # Path to second frame of anim

        self.scr_width: int = scr_w
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed: int = speed
        self.ready: bool = True

        self.shooting_time: int = 0
        self.shoot_cd: int = 600
        self.projectiles = pg.sprite.Group()
        self.shot_sound = pg.mixer.Sound(
            "./resources/audio/shot.wav")
        self.shot_sound.set_volume(0.5)

        # Images for going right or left
        self.right_dir = self.image  # No flip
        self.left_dir = pg.transform.flip(  # Flip
            self.image, True, False)

        self.current_side = "right"

        # Animation section:
        self.current_frame = 0
        self.current_time = 0
        self.available_frames = [self.sprite_path, self.second_frame_path]

    def player_input(self) -> None:
        """Player input mapping"""

        keys = pg.key.get_pressed()

        """If right arrow is pressed and held, player moves to right"""
        """If left arrow is pressed and held, player moves to left"""

        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed
            self.current_side = "right"
            self.image = self.right_dir

        elif keys[pg.K_LEFT]:
            self.rect.x -= self.speed
            self.current_side = "left"
            self.image = self.left_dir

        """Shoots projectile if SPACE is pressed"""

        if keys[pg.K_SPACE] and self.ready:
            self.shoot()
            self.ready = False
            self.shooting_time = pg.time.get_ticks()

    def update(self) -> None:
        self.player_input()
        self.clamp()
        self.reload()
        self.projectiles.update()

    def reload(self) -> None:
        """Enables shooting if no player projectile is present"""

        if not self.ready and not self.projectiles:
            self.ready = True

    def clamp(self) -> None:
        """Locks player on screen"""

        if self.rect.left <= 0:  # if left pos <= 0, pos is set to 0
            self.rect.left = 0
        elif self.rect.right >= self.scr_width:  # if right pos >= scr_width, pos is set to scr_width
            self.rect.right = self.scr_width

    def shoot(self) -> None:
        self.projectiles.add(Projectile(
            self.rect.center, "./resources/cannon_ball.png", 8, self.rect.bottom))
        self.shot_sound.play()
