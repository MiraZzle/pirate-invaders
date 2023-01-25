"""Main script responsible for managing the game. All other scripts are handled from here as modules."""

import os
import sys
import pygame as pg

# game objects
import wall
from score_manager import HighScoreManager
from enemy import Enemy
from enemy import BonusEnemy
from player import Player
from projectile import Projectile

# utilities
from random import randint
from random import choice
from pathlib import Path

# parent directory of current file parent directory
app_folder = os.path.dirname(os.path.dirname(__file__))

# Class for all game processes:


class GameLoop:
    def __init__(self) -> None:
        # create player object
        player_sprite = Player((scr_width / 2, scr_height), scr_width, 5)
        #  GroupSingle = container holding only one object (player), simplifies updating and drawing the player
        self.player = pg.sprite.GroupSingle(player_sprite)

        # Sets os window icon and name:
        self.window_icon = pg.image.load(app_folder + "/resources/im1.png")

        pg.display.set_icon(self.window_icon)
        pg.display.set_caption("Pirate Defence")

        # Sets main background music:
        self.main_music = pg.mixer.Sound(app_folder +
                                         "/resources/audio/main_music.wav")  # creates new sound object for main background music
        self.main_music.set_volume(0.4)
        self.main_music.play(-1)  # Arg -1 loops music

        # Sound effect for projectile based collisions:
        self.collision_sound = pg.mixer.Sound(app_folder +
                                              "/resources/audio/collision.wav")  # creates new sound object for collision event
        self.collision_sound.set_volume(0.5)

        # Sound effect for projectile init:
        self.shot_sound = pg.mixer.Sound(app_folder +
                                         "/resources/audio/shot.wav")  # creates new sound object for shoot event
        self.shot_sound.set_volume(0.5)

        # Sound effect for game over:
        self.game_over_sound = pg.mixer.Sound(app_folder +
                                              "/resources/audio/game_over.wav")
        self.shot_sound.set_volume(0.5)

        # Lives section:
        self.lives: int = 3
        self.live_icon = pg.image.load(app_folder +
                                       "/resources/im5.png").convert_alpha()
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
        # Container for walls, allows mass updating
        self.walls = pg.sprite.Group()
        self.wall_amount: int = 5  # How many walls are used

        # calculate positions of wall objects
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
        self.bg = pg.image.load(
            app_folder+"/resources/big_bg.png").convert()  #  load bg file, convert() = optimize image for faster blitting
        self.font = pg.font.Font(app_folder+"/fonts/pixel_8fj.ttf", 30)

    # Wall methods section:

    def spawn_wall(self, x_start_pos, y_start_pos, x_offset) -> None:
        """Creates a wall using shape defined in separate script, if "X" is detected in matrix, the cell is filled with color and properly sized"""

        # loops through rows in wall shape (=matrix)
        for r_index, row in enumerate(self.wall_shape):
            for c_index, col in enumerate(row):  # loops through columns in row
                if col == "X":
                    block = wall.Wall(
                        self.cell_size, (23, 23, 23), x_start_pos + c_index * self.cell_size + x_offset, y_start_pos + r_index * self.cell_size)
                    # add block object to walls container
                    self.walls.add(block)

    def place_walls(self, *offset, x_pos, y_pos) -> None:
        """Spawns walls at given positions with offset = distance inbetween"""

        for x in offset:
            self.spawn_wall(x_pos, y_pos, x)

    def empty_walls(self) -> None:
        """Clears group walls, used for next_round() or new game"""

        self.walls.empty()  #  clear walls container

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
                #  add enemy object to enemies container
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
        """"Chooses random enemy from list and inits new projectile at his coords"""

        if self.enemies.sprites():
            if self.dead == False:
                #  returns random sprite from enemies container
                rand_enemy = choice(self.enemies.sprites())

                arrow_sprite = Projectile(
                    rand_enemy.rect.center, app_folder + "/resources/arrow.png", -6, scr_height)

                self.enemy_projectiles.add(arrow_sprite)
                self.shot_sound.play()

    def bonus_enemy_timer(self) -> None:
        """Spawns bonus enemy"""

        self.bonus_spawn_t -= 1
        if self.bonus_spawn_t <= 0:
            self.bonus_enemies.add(BonusEnemy(
                choice(["right", "left"]), scr_width))
            #  set time for bonus enemy spawn to interval <600,1000>
            self.bonus_spawn_t = randint(600, 1000)

    def collision_checker(self) -> None:
        """Handles all collisions"""

        # Checs for player projectile collisions
        if self.player.sprite.projectiles:
            for projectile in self.player.sprite.projectiles:  #  loop through all sprites in projectiles container

                if pg.sprite.spritecollide(projectile, self.walls, True):
                    # removes projectile from all groups, makes it unresponsive and stops drawing the sprite
                    projectile.kill()

                enemies_hit = pg.sprite.spritecollide(
                    projectile, self.enemies, True)  # checks for collision between projectile and enemies group, True param means that member of self.enemies is deleted on collision with projectile, returns list of collider enemies

                if enemies_hit:
                    for enemy in enemies_hit:
                        self.score += enemy.value  #  add specific value to score
                        self.collision_sound.play()
                    projectile.kill()

                # checks for collision between projectile and bonus enemies group, kills bonus enemy on collision
                if pg.sprite.spritecollide(projectile, self.bonus_enemies, True):
                    projectile.kill()
                    self.score += self.bonus_enemy_value

        # Checks for enemy projectile collisions
        if self.enemy_projectiles:
            for projectile in self.enemy_projectiles:

                if pg.sprite.spritecollide(projectile, self.walls, True):
                    projectile.kill()

                # If enemy projectile collides with player, sub 1 life
                if pg.sprite.spritecollide(projectile, self.player, False):
                    projectile.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over()
                        self.high_score_manager.check_highcore(
                            self.score)  #  compare current HS to saved HS

                if pg.sprite.spritecollide(projectile, self.walls, True):
                    projectile.kill()

        # Checks for enemy collisions
        if self.enemies:
            for enemy in self.enemies:
                # Deletes wall blocks on collision
                pg.sprite.spritecollide(enemy, self.walls, True)

                # Game over if enemy collides with player
                if pg.sprite.spritecollide(enemy, self.player, False):
                    self.high_score_manager.check_highcore(self.score)
                    self.game_over()

    def show_lives(self) -> None:
        """Renders n-1 lives left"""

        mess_to_show = "LIVES: "
        # creates new text surface with given text, without anti aliasing in white color
        lives_text = self.font.render(mess_to_show, False, "white")
        lives_rect = lives_text.get_rect(center=(620, 30))
        screen.blit(lives_text, lives_rect)  # blits rendered message on rect

        for icon in range(self.lives - 1):  #  sets visible amount of lives left
            x = self.live_pos_x + (icon * self.live_icon.get_size()[0] + 10)
            screen.blit(self.live_icon, (x, 8))  #  blits left lives

    def show_score(self) -> None:
        """Shows current score"""

        score_to_show = "SCORE: " + str(self.score)
        score_txt = self.font.render(score_to_show, False, "white")
        score_rect = score_txt.get_rect(center=(145, 30))
        screen.blit(score_txt, score_rect)

    def show_high_score(self) -> None:
        """Shows current HS"""

        score_to_show = "HS: " + str(self.high_score)
        score_txt = self.font.render(score_to_show, False, "white")
        score_rect = score_txt.get_rect(center=(scr_width/2, 30))
        screen.blit(score_txt, score_rect)

    def next_round(self) -> None:
        """If enemies group is empty, initiated new wave of enemies"""

        if not self.enemies:  # if enemies container is empty -> new round to be spawned
            if not self.dead:
                self.empty_walls()
                self.spawn_enemies(5, 10)
                self.place_walls(*self.wall_x_positions,
                                 x_pos=scr_width/16, y_pos=480)

    def game_over(self) -> None:
        """Empties all groups"""

        self.main_music.stop()
        self.player.sprite.projectiles.empty()
        self.enemy_projectiles.empty()
        self.enemies.empty()
        self.empty_walls()
        self.player.empty()
        self.bonus_enemies.empty()

        self.high_score_manager.check_highcore(self.score)
        self.game_over_sound.play()
        self.dead = True

    def death_message(self, message_to_render, new_game_instructions, score_line):
        """Display message after game over"""

        mess_offset = 60
        messages = [message_to_render, new_game_instructions, score_line]
        #  vertically blits rendered text surfaces on temp_rect
        for i, message in enumerate(messages):
            temp_mess = self.font.render(message, False, "white")
            temp_rect = temp_mess.get_rect(
                center=(scr_width / 2, mess_offset * i + scr_height / 2 - 40))
            screen.blit(temp_mess, temp_rect)

    def new_game(self) -> None:
        """Inits new game"""

        self.__init__()  #  reset all values

    def run(self) -> None:
        """Main handler method, runs every tick"""

        self.update()
        self.all_draw()
        self.all_checks()
        self.check_for_death_mess()

        self.enemy_stack = self.enemies.sprites()

    def update(self) -> None:
        """Updates all objects"""

        if self.dead == False:
            self.player.update()
            self.enemies.update(self.enemy_dir)
            self.enemy_projectiles.update()
            self.bonus_enemies.update()

    def check_for_death_mess(self):
        """Checks to display death message and new game instructions"""
        if self.dead == False:
            self.death_message("", "", "")
        else:
            self.death_message("GAME OVER",
                               "SCORE: " + str(self.score),
                               "press ENTER to RESTART")
            keys = pg.key.get_pressed()  # returns list of all keyboard keys states

            if keys[pg.K_RETURN]:
                self.__init__()

    def all_draw(self) -> None:
        """Draws all objects on screen"""
        self.enemy_projectiles.draw(screen)
        self.walls.draw(screen)
        self.enemies.draw(screen)
        self.bonus_enemies.draw(screen)

        if self.player:
            self.player.draw(screen)
            self.player.sprite.projectiles.draw(screen)

    def all_checks(self) -> None:
        """Custom checks"""

        if self.player:
            self.collision_checker()

        self.enemy_pos_check()
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
    enemy_proj_cd: int = 1200

    clock = pg.time.Clock()  # create clock object
    screen = pg.display.set_mode(
        (scr_width, scr_height))  #  crete new display surface, everything is drawn on it
    game = GameLoop()

    enemy_projectile = pg.USEREVENT + 1  #  custom event
    #  set time enemy_projectile event
    pg.time.set_timer(enemy_projectile, enemy_proj_cd)

    while active_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Window close
                active_game = False
                pg.quit()  #  uninitialize all pygame modules, frees all resources, clean quit before sys.exit()
                sys.exit()  #  exit program

            if event.type == enemy_projectile:  # Inits enemy projectile
                game.enemy_shoot()

        screen.blit(game.bg, (0, 0))  # Sets gamebackground with (0,0) offset
        game.run()  # Runs all functions

        pg.display.flip()
        clock.tick(60)  # Sets to 60 FPS


if __name__ == "__main__":  # checks if script is not run as module
    main()
