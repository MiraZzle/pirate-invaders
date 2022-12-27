import pygame as pg
import sys
import wall

from score_manager import HighScoreManager
from enemy import Enemy
from enemy import BonusEnemy
from player import Player
from projectile import Projectile

from random import randint
from random import choice


class GameLoop:
    def __init__(self) -> None:
        player_sprite = Player((scr_width / 2, scr_height), scr_width, 5)
        self.player = pg.sprite.GroupSingle(player_sprite)

        # Sets os window icon and name:
        self.window_icon = pg.image.load("./resources/im1.png")

        pg.display.set_icon(self.window_icon)
        pg.display.set_caption("Pirate Defence")

        # Sets main background music:
        self.main_music = pg.mixer.Sound(
            "./resources/audio/main_music.wav")
        self.main_music.set_volume(0.4)
        self.main_music.play(-1)  # Arg -1 loops music

        # Sound effect for projectile based collisions:
        self.collision_sound = pg.mixer.Sound(
            "./resources/audio/collision.wav")
        self.collision_sound.set_volume(0.5)

        # Sound effect for projectile init:
        self.shot_sound = pg.mixer.Sound(
            "./resources/audio/shot.wav")
        self.shot_sound.set_volume(0.5)

        self.lives: int = 3
        self.live_icon = pg.image.load(
            "./resources/im5.png").convert_alpha()
        self.live_pos_x = scr_width - (self.live_icon.get_size()[0] * 2 + 20)
        self.dead: bool = False

        # Score section:
        self.score = 0
        # Inits HSManager, which checks for new HS and saves it in .txt
        self.high_score_manager = HighScoreManager()
        self.high_score = self.high_score_manager.get_highscore()

        # Destructable walls / obstacles section:
        self.wall_shape = wall.shape
        # self.cell_size = how many pixels is a grid cell (=1 grid pixel) worth
        self.cell_size: int = 6
        self.walls = pg.sprite.Group()  # Groups all used walls
        self.wall_amount: int = 5  # How many walls are used
        self.wall_x_positions = [n * (scr_width / self.wall_amount)
                                 for n in range(self.wall_amount)]
        self.place_walls(*self.wall_x_positions, x_pos=scr_width/16, y_pos=480)

        # Enemies section:
        self.enemies = pg.sprite.Group()  # Allows to update all enemies
        self.spawn_enemies(rows=5, cols=10)
        self.enemy_dir: int = 1  # Starting direction of enemies = right

        self.enemy_stack = self.enemies.sprites()  # List of enemies, used in loops
        self.enemy_projectiles = pg.sprite.Group()  #  Groups enemy projectiles

        self.bonus_enemies = pg.sprite.GroupSingle()  # Stores bonus enemy ("captain")
        # Random time to spawn next bonus
        self.bonus_spawn_t: int = randint(600, 1000)
        self.bonus_enemy_value: int = 600

        # Extras section:
        self.bg = pg.image.load("./resources/big_bg.png").convert()
        self.font = pg.font.Font("./fonts/pixel_regular.ttf", 20)

    # Wall methods section:

    def spawn_wall(self, x_start_pos, y_start_pos, x_offset) -> None:
        """Creates a wall using shape defined in separate script, if "X" is detected in matrix, the cell is filled with color and properly sized"""

        # loops through rows in wall shape (=matrix)
        for r_index, row in enumerate(self.wall_shape):
            for c_index, col in enumerate(row):  # loops through columns in row
                if col == "X":
                    block = wall.Wall(
                        self.cell_size, (23, 23, 23), x_start_pos + c_index * self.cell_size + x_offset, y_start_pos + r_index * self.cell_size)
                    self.walls.add(block)

    def place_walls(self, *offset, x_pos, y_pos) -> None:
        """Spawns walls at given positions with offset = distance inbetween"""

        for x in offset:
            self.spawn_wall(x_pos, y_pos, x)

    def empty_walls(self) -> None:
        """Clears group walls, used for next_round() or new game"""

        self.walls.empty()

    # Enemy methods section:
    def spawn_enemies(self, rows, cols, x_dist=55, y_dist=48, x_offset=70, y_offset=140) -> None:
        """Similar to spawn_wall(), adds enemy to given place in matrix, currently 5x10, x_offset and y_offset dictate upper left corner pos, enemy at (0,0) has these pos values"""

        for r_index, row in enumerate(range(rows)):
            for c_index, col in enumerate(range(cols)):
                x = x_offset + c_index * x_dist
                y = y_offset + r_index * y_dist

                if r_index == 0:  # First row has type 3 enemy
                    enemy_sprite = Enemy("im3", x, y)
                elif 1 <= r_index <= 2:  # Second and third row has type 2 enemy
                    enemy_sprite = Enemy("im2", x, y)
                else:  # Fourth and fifth row has type 4 enemy
                    enemy_sprite = Enemy("im4", x, y)
                self.enemies.add(enemy_sprite)

    def enemy_pos_check(self) -> None:
        """Checks for the most left and right enemy pos, if one is at the border of screen, every enemy moves down 2 and changes direction"""

        for enemy in self.enemy_stack:
            if enemy.rect.right >= scr_width:
                self.enemy_dir = -1
                self.enemy_mv_down()

            elif enemy.rect.left <= 0:
                self.enemy_dir = 1
                self.enemy_mv_down()

    def enemy_mv_down(self) -> None:
        """If enemies group is not empty, every item moved"""

        if self.enemies:
            for enemy in self.enemy_stack:
                enemy.rect.y += 2

    def enemy_shoot(self) -> None:
        if self.enemies.sprites():
            """"Chooses random enemy from list and inits new projectile at his coords"""

            rand_enemy = choice(self.enemies.sprites())

            arrow_sprite = Projectile(
                rand_enemy.rect.center, "./resources/arrow.png", -5, scr_height)

            self.enemy_projectiles.add(arrow_sprite)
            self.shot_sound.play()

    def bonus_enemy_timer(self) -> None:
        """Spawns bonus enemy"""

        self.bonus_spawn_t -= 1
        if self.bonus_spawn_t <= 0:
            self.bonus_enemies.add(BonusEnemy(
                choice(["right", "left"]), scr_width))
            self.bonus_spawn_t = randint(600, 1000)

    def collision_checker(self) -> None:
        if self.player.sprite.projectiles:
            for projectile in self.player.sprite.projectiles:
                if pg.sprite.spritecollide(projectile, self.walls, True):
                    projectile.kill()

                enemies_hit = pg.sprite.spritecollide(
                    projectile, self.enemies, True)
                if enemies_hit:
                    for enemy in enemies_hit:
                        self.score += enemy.value
                        self.collision_sound.play()
                    projectile.kill()

                if pg.sprite.spritecollide(projectile, self.bonus_enemies, True):
                    projectile.kill()
                    self.score += self.bonus_enemy_value

        if self.enemy_projectiles:
            for projectile in self.enemy_projectiles:
                if pg.sprite.spritecollide(projectile, self.walls, True):
                    projectile.kill()

                if pg.sprite.spritecollide(projectile, self.player, False):
                    projectile.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.dead = True
                        self.high_score_manager.check_highcore(self.score)

                if pg.sprite.spritecollide(projectile, self.walls, True):
                    projectile.kill()

        if self.enemies:
            for enemy in self.enemies:
                pg.sprite.spritecollide(enemy, self.walls, True)

                if pg.sprite.spritecollide(enemy, self.player, False):
                    self.high_score_manager.check_highcore(self.score)

    def show_lives(self) -> None:
        """Renders n-1 lives left"""

        for icon in range(self.lives - 1):
            x = self.live_pos_x + (icon * self.live_icon.get_size()[0] + 10)
            screen.blit(self.live_icon, (x, 8))

    def show_score(self) -> None:
        """Shows current score"""

        score_to_show = "SCORE: " + str(self.score)
        score_txt = self.font.render(score_to_show, False, "white")
        score_rect = score_txt.get_rect(topleft=(10, 10))
        screen.blit(score_txt, score_rect)

    def show_high_score(self) -> None:
        """Shows current HS"""

        score_to_show = "HS: " + str(self.high_score)
        score_txt = self.font.render(score_to_show, False, "white")
        score_rect = score_txt.get_rect(center=(scr_width/2, 30))
        screen.blit(score_txt, score_rect)

    def next_round(self) -> None:
        """If enemies group is empty, initiated new wave of enemies"""

        if not self.enemies:
            self.empty_walls()
            self.spawn_enemies(5, 10)
            self.place_walls(*self.wall_x_positions,
                             x_pos=scr_width/16, y_pos=480)

    def loss_message(self) -> None:
        self.dead = True
        self.enemies.empty()
        self.empty_walls()
        self.high_score_manager.check_highcore(self.score)

        message = self.font.render("GAME OVER", False, "white")
        mess_rect = message.get_rect(
            center=(scr_width / 2, scr_height / 2))
        screen.blit(message, mess_rect)

    def new_game(self) -> None:
        self.__init__()

    def run(self) -> None:
        """Main handler method, runs every tick"""

        self.update()
        self.all_draw()
        self.all_checks()

        self.enemy_stack = self.enemies.sprites()

    def update(self) -> None:
        """Updates all objects"""

        if self.dead == False:
            self.player.update()
            self.enemies.update(self.enemy_dir)
            self.enemy_projectiles.update()
            self.bonus_enemies.update()

    def all_draw(self) -> None:
        """Draws all objects on screen"""

        self.player.draw(screen)
        self.player.sprite.projectiles.draw(screen)
        self.enemy_projectiles.draw(screen)
        self.walls.draw(screen)
        self.enemies.draw(screen)
        self.bonus_enemies.draw(screen)

    def all_checks(self) -> None:
        """Custom checks"""

        self.enemy_pos_check()
        self.collision_checker()
        self.next_round()
        self.bonus_enemy_timer()
        self.show_lives()
        self.show_score()
        self.show_high_score()


def main() -> None:
    """Main function"""

    global scr_width
    global scr_height
    global screen

    pg.init()
    active_game: bool = True
    scr_width = 800
    scr_height = 600

    clock = pg.time.Clock()
    screen = pg.display.set_mode(
        (scr_width, scr_height))
    game = GameLoop()

    enemy_projectile = pg.USEREVENT + 1
    pg.time.set_timer(enemy_projectile, 1200)

    while active_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Window close
                active_game = False
                pg.quit()
                sys.exit()

            if event.type == enemy_projectile:  # Inits enemy projectile
                game.enemy_shoot()

        screen.blit(game.bg, (0, 0))  # Sets gamebackground with (0,0) offset
        game.run()  # Runs all functions

        pg.display.flip()
        clock.tick(60)  # Sets to 60 FPS


if __name__ == "__main__":
    main()
