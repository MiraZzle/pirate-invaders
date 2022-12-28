# Pirate Invaders

##Gameplay
###Description
Pirate Invaders is a game based on the game Space Invaders. The player controls a horizontally moving character. 
Players Goal is to achieve the highest score by eliminating enemy entities.

###Entities
- Player 
  - Moves horizontally and shoots a projectile to destroy enemies. The player has 3 lives, which are lost by colliding with enemy 
projectiles or colliding with enemy entity.

- Enemy 
  - Moves horizontally in a group. If a member of enemy group touches a side of the game window, the enemy group switches direction. 
Randomly fires a projectile. On collision subtracts a player life or deletes a piece of wall. 
There are 3 enemy types, which differ in points given after their destruction by player.

- Bonus Enemy 
  - Moves horizontally. Spawns on top of the screen at random time. Gives bonus points if destroyed.

- Wall
  - Static entity. Protects the player from enemy projectiles. This entitity can be destroyed by colliding with any projectiles.

##Controls

##Game Over

