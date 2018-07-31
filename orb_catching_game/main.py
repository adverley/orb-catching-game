from orb_catching_game.game import OrbCatchingGame

if __name__ == '__main__':
    level = 1

    settings = {
    "screen_resolution": [512,512],
    "robot_speed": 10,
    "robot_size": [20,20],
    "orb_size": [10,10],
    "obstacle_size": [30,30],
    "spawn_distance_ratios": {
      "obstacle-obstacle": 2,
      "obstacle-robot": 2,
      "obstacle-orb": 2.5,
      "robot-orb": 1,
      "orb-orb": 1
    },
    "n_obstacles": 7,
    "n_bonus_orbs": 3
  }

    game = OrbCatchingGame(level, settings)
    game.on_execute()
