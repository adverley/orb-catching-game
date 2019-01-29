
import random
import numpy as np
from gym.spaces import Discrete

from orb_catching_game.orb  import BonusOrb
from orb_catching_game.game import OrbCatchingGame
from orb_catching_game.robot import Robot
from PIL import Image
import scipy.spatial.distance as dist
import PIL
from IPython.display import clear_output


class OrbCatchingEnvironment():
    DISPLAY_SIZE = (128,128)
    
    def __init__(self, reward_function=lambda _: 0, level=1) -> None:
        super().__init__()
        self.level = level
        self.viewer = None
        self.steps_taken = 0

        self.game = OrbCatchingGame(level)
        while self.game.on_init() == False:
            # wait for it
            pass

        self.action_space = Discrete(4)

        self.observation_space = None

        self.state = None

        self.game.step()

        self.input_shape = tuple(self.game.size)

        self.n_bonus_orbs_rewards_assigned = 0
        
        self.reward = reward_function

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        Args:
            action (object): an action provided by the environment
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        self.game.step(action)

        obs = self.get_current_state()
        reward = self.reward(self.game)
        done = self.game.normal_orb_is_caught()

        self.steps_taken += 1
        self.state = obs
        return obs, reward, done, {}
    
    """Resets the state of the game. This should be called manually after an environment.step() returns a terminal state.
    Args:
        with_robot (boolean): if True, the robot will be spawned at a different place, 
                                else the robot will remain at the same location.
    Returns:
        the state of the resetted environment.
    """
    def reset(self, with_robot=False):
        self.game.reset()
        if with_robot:
            self.game.respawn_robot()

        self.game.step(Robot.ACTION_NOTHING)
        self.n_bonus_orbs_rewards_assigned = 0
        self.steps_taken = 0

        self.state = self.get_current_state()
        return self.state
    
    def render(self, mode='rgb'):
        frame = self.game.get_last_frame()
        img = Image.frombytes('RGB', self.input_shape, frame)
        img = np.array(img)
        
        display(PIL.Image.fromarray(img).resize(OrbCatchingEnvironment.DISPLAY_SIZE, Image.ANTIALIAS))
        clear_output(wait=True)
        return img

    def close(self):
        self.game.on_cleanup()
        if self.viewer is not None: self.viewer.close()

    def get_current_state(self):
        return self.game.get_last_frame()
    
    @property
    def orbs_caught(self):
        return self.n_bonus_orbs_rewards_assigned + self.game.normal_orb_is_caught()