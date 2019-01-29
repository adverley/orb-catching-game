# Orb Catching Game
In this game a robot has to catch an orb which will change position when it is caught. There are three levels with increasing difficulty. This game is developed for RL purposes.

## Getting started
Install with `pip install git+https://github.com/adverley/orb-catching-game`. 
You can [play the game yourself](#playing-the-game).

The game is primarily meant for Reinforcement Learning purposes. I recommend embedding the game in a [Gym](https://github.com/openai/gym/blob/master/gym/core.py) Environment (the Env class). There is an example in the [orb_catching_env.py](https://github.com/adverley/orb-catching-game/blob/master/orb_catching_game/utilities/orb_catching_env.py) file. 

## Levels 
### Level 1
In this level, the robot operates in a 10x10 grid and can move in four directions: up, down, left, right. Once the robot touches the golden orb, he receives a point and the orb is respawned at a different location. The robot does not resemble a triangle here due to rescaling the 10x10 image.

### Level 2
Level 2 operates on the same principles as level 1 with the two main differences. First, the robot now has two obstacles blocking the way towards the orb. The second difference is that when the robot touches both obstacles, a red bonus orb is spawned which is worth much more compared to the regular, golden orb. The bonus orb is removed when the robot catches it or in case the robot first captures the regular orb, the bonus orb is removed and the regular orb and obstacles respawned at different locations. 

### Level 3
In level 3, we scale up the grid of the robot from 10x10 to 50x50 and introduce three obstacles. In case the robot touches all three obstacles, three bonus orbs are released randomly in to the grid. The same (re-)spawning rules as in level 2 apply. 

## Playing the game
The game runs by default headless without keyboard event handling. You can play it yourself by setting `PLAY_SELF = True` in [game.py](https://github.com/adverley/orb-catching-game/blob/master/orb_catching_game/game.py). I would also recommend choosing level 3 so the rendered surface is `[50, 50]` by running 
```
game = OrbCatchingGame(level=3) 
game.on_execute()
``` 
or change the screen resolution in the [settings](https://github.com/adverley/orb-catching-game/blob/master/orb_catching_game/SETTINGS.json).

