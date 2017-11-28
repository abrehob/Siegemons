# Siegemons

Hello! This repository contains the data necessary to run the "183 Siege" project and the "Siegemons" extension created in Winter 2015.

Background:  
In Winter 2015, I took a class called Elementary Programming Concepts (EECS 183) at the University of Michigan. At the end of the semester, all students were required to create a group project with 3 other students. The final project that my team decided to do was called "183 Siege". Almost all of the code for this project was written by EECS 183 instructors; all that was required of my team was to implement an artificially intelligent agent that would complete the game as efficiently as possible. After my team completed the core requirements, I decided to extend the existing source code to create a cross between "183 Siege" and "Pokemon".

## 183 Siege:

In this game, you must travel through a dungeon and attempt to go down as many floors as you can. There are two main parts to the game: traverse the map using "wasd" controls or using "x" to follow a pre-implemented path-finding algorithm, and battling monsters.

### Travelling across the dungeon map:

Symbol key:  
x: Player icon  
\#: Wall  
=: Door  
@: Stairs (to next floor)  

At the top, there is a bunch of information including floor number, player health, chance of getting into an encounter, and many one-use items.

Actions:  
w: move up  
a: move left  
s: move down  
d: move right  
x: auto-move towards stairs  
h: hide  
q: exit program  

### Battling monsters:

Whenever you choose to take a step in the map or spend a turn to hide, there is a chance you will enter an encounter. When this happens, the screen layout changes to the battle screen. At the top bar of this screen, you can see information related to the actions taken in the battle. In the bottom-left, you can view your weapons' names, strengths, and durabilities. In the bottom-right, you can see information related to the enemy, your current weapon, and your inventory.

Actions:  
x: fight  
c: defend  
1: switch weapon  
i: potion  
e: attempt to escape  
f: use fireball  
q: exit program

### Running the program:

Open a Terminal window (I'm assuming you're using a Mac) and enlarge it to fill the screen. After cloning this repository and entering the top-level directory, execute the following commands:  
`cd FP_siege_abrehob_becgabri_kreault_smokhtar/`  
`python2.7 ./driver.py`

By default, the AI will run for the program. It runs relatively fast, so you can press the "Enter" key to stop the AI and look back at what it did. You can let the AI continue to run if you press the "Enter" key again (you might have to press it twice).  
If you want to play the game yourself, just edit the top of the "ai.py" file and change "USE_AI = True" to "USE_AI = False".

## Siegemons:

Travelling across the dungeon map is no different from 183 Siege.

### Battling monsters:

Encounters are almost exactly the same as in 183 Siege except for a couple of things:  
You don't use weapons with attack power and durability, but rather Siegemons with level and health  
When you battle, instead of you getting damaged, your active Siegemon gets damaged  
When you win a battle, you have the option of having the opposing fainted Siegemon join your team (with full health)

### Running the program:

Open a Terminal window and enlarge it to fill the screen. Execute the following commands:  
`cd Siegemons/Siegemons\ Data/`  
`python2.7 ./driver.py`

Note: there is no AI for this game.
