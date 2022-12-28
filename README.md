# Pirate Invaders

## Gameplay

### Description
Pirate Invaders is a game based on the game Space Invaders. The player controls a horizontally moving character. 
Players Goal is to achieve the highest score by eliminating enemy entities.

<img width="631" alt="Snímek obrazovky 2022-12-28 v 17 43 24" src="https://user-images.githubusercontent.com/65544540/209844778-1e281ecd-6ad7-4332-b873-fb2808e2b480.png">

## How to play
1. Clone the repository
2. Run the file ./source_code/main.py

## Entities

- Player 
  - Moves horizontally and shoots a projectile to destroy enemies. The player has 3 lives, which are lost by colliding with enemy 
projectiles or colliding with enemy entity.  
  ![im5](https://user-images.githubusercontent.com/65544540/209845408-95261caa-8c39-4058-a1d9-bf5dd80326f0.png)


- Enemy 
  - Moves horizontally in a group. If a member of enemy group touches a side of the game window, the enemy group switches direction. 
Randomly fires a projectile. On collision subtracts a player life or deletes a piece of wall. 
There are 3 enemy types, which differ in points given after their destruction by player.
  ![im2](https://user-images.githubusercontent.com/65544540/209845436-2794e568-0bef-4601-b658-734ded81bf5f.png)
  ![im3](https://user-images.githubusercontent.com/65544540/209845439-fcd67d27-c875-4971-8c1f-36eff67e0fcf.png)
  ![im4](https://user-images.githubusercontent.com/65544540/209845448-059f4ef9-8848-412e-a9b4-34a9f3513b7b.png)
- Bonus Enemy 

  - Moves horizontally. Spawns on top of the screen at random time. Gives bonus points if destroyed.
  ![im1](https://user-images.githubusercontent.com/65544540/209845295-74f8c75d-f473-499f-adfd-2df83b8b19e7.png)

- Wall
  - Static entity. Protects the player from enemy projectiles. This entitity can be destroyed by colliding with any projectiles.

## Controls

### Player controller
- To move the player use the following controls: 
  -  Hold → to move right
  -  Hold ← to move left
  -  Press **space** to shoot a projectile


## Game Over
- Player 

