# Pirate Invaders

## Gameplay

### Description
Pirate Invaders is a game based on the game Space Invaders. The player controls a horizontally moving character. 
Players goal is to achieve the highest score by eliminating enemy entities.

<p align="center">
<img width="631" alt="Snímek obrazovky 2022-12-28 v 17 43 24" src="https://user-images.githubusercontent.com/65544540/209844778-1e281ecd-6ad7-4332-b873-fb2808e2b480.png">
</p>

## Prerequisities
1. [Download Python](https://www.python.org/downloads/) (v3.10+)
2. [Download Pygame](https://pypi.org/project/pygame/) (v2.1.2)

## How to play
1. Clone the repository
2. Open the **ENTIRE** repository in IDE
3. Run the file ./source_code/main.py

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

### Player controller
- To move the player use the following controls: 
  -  Hold **→**(**LEFT ARROW KEY**) to move right
  -  Hold **←** (**RIGHT ARROW KEY**) to move left
  -  Press **SPACE** to shoot a projectile

### New game
- Press **ENTER** after the game is over to restart the game

## UI
- UI displays:
  - Current score:
  <img width="218" alt="Snímek obrazovky 2022-12-28 v 18 40 30" src="https://user-images.githubusercontent.com/65544540/209851357-ea7f99b5-3871-491f-8894-296f251d526f.png">
  
  - Highscore:
   <img width="110" alt="Snímek obrazovky 2022-12-28 v 18 40 35" src="https://user-images.githubusercontent.com/65544540/209851346-768daf46-ecea-4fd7-9b82-1db16b131da3.png">
  
  - Lives left:
   <img width="205" alt="Snímek obrazovky 2022-12-28 v 17 46 00" src="https://user-images.githubusercontent.com/65544540/209851194-71d79f5c-9429-4b45-96ab-665a833c895c.png">


## Game Over
- Game Over conditions:
  - Game ends if player health reaches 0
  - Game ends if player collides with an enemy
 
 <p align="center">
  <img width="363" alt="Snímek obrazovky 2022-12-28 v 17 56 27" src="https://user-images.githubusercontent.com/65544540/209846303-49c9aa5c-6721-4355-a895-6d1798fb6480.png">
</p>

