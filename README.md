# Pirate Invaders
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

## About the project
Pirate Invaders is a game based on the game Space Invaders. The player controls a horizontally moving character. 
Players goal is to achieve the highest score by eliminating enemy entities.

## Prerequisities
1. [Download Python](https://www.python.org/downloads/) (v3.10+)
2. [Download Pygame](https://pypi.org/project/pygame/) (v2.1.2)

## How to play
1. Clone this repository or download it as a ZIP file
      ```bash
   git clone https://github.com/MiraZzle/pirate-invaders
   ```
2. Open the project in an IDE of your choice
3. Run the ./source_code/main.py

## Launching from Terminal
- To run the game from Terminal, make sure your current working directory is ```pirate_invaders```. From terminal, run this command: 
```
python3 ./source_code/main.py
```

## Entities

- **Player** ![im5](https://user-images.githubusercontent.com/65544540/209845408-95261caa-8c39-4058-a1d9-bf5dd80326f0.png)
  - Moves horizontally and shoots a projectile to destroy enemies. The player has 3 lives, which are lost by colliding with enemy 
projectiles or colliding with enemy entity.  
  


- **Enemy** ![im2](https://user-images.githubusercontent.com/65544540/209845436-2794e568-0bef-4601-b658-734ded81bf5f.png)![im3](https://user-images.githubusercontent.com/65544540/209845439-fcd67d27-c875-4971-8c1f-36eff67e0fcf.png)![im4](https://user-images.githubusercontent.com/65544540/209845448-059f4ef9-8848-412e-a9b4-34a9f3513b7b.png)
  - Moves horizontally in a group. If a member of enemy group touches a side of the game window, the enemy group switches direction. 
Randomly fires a projectile. On collision enemy projectile subtracts a player life or deletes a piece of wall. 
There are 3 enemy types, which differ in points given after their destruction by player.
  
  
  
- **Bonus Enemy** ![im1](https://user-images.githubusercontent.com/65544540/209845295-74f8c75d-f473-499f-adfd-2df83b8b19e7.png)
  - Moves horizontally. Spawns on top of the screen at random time. Gives bonus points if destroyed.
  

- **Wall**
  - Static entity. Protects the player from enemy projectiles. This entitity can be destroyed by colliding with any projectiles. Resets every new round.

## Controls

| Key                  | Action             |
| ---------------------| -------------------|
| <kbd>→</kbd>         | Move Right         |
| <kbd>←</kbd>         | Move Left          |
| <kbd>Space</kbd>     | Shoot              |
| <kbd>Enter</kbd>     | Restart Game       |

## Game Over
- Game Over conditions:
  - Game ends if player health reaches 0
  - Game ends if player **collides** with an enemy
