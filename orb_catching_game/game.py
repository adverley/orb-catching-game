PLAY_SELF = 0

HEADLESS = True and not PLAY_SELF

# TODO: respawn orb without killing it! Just respawn the position

import os

# RUN THIS BEFORE IMPORTING PYGAME
if HEADLESS:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

from orb_catching_game.floor import Floor
from orb_catching_game.obstacle import Obstacle
from orb_catching_game.orb import Orb, BonusOrb
from orb_catching_game.robot import Robot
from orb_catching_game.utilities import files

import pygame
from pygame.locals import *
import random
from pygame.sprite import collide_rect_ratio, spritecollideany


class OrbCatchingGame:
    STATE_NORMAL = 0
    STATE_BONUS = 1

    def __init__(self, level=1):
        self._running = True
        self._display_surface = None
        self.state = OrbCatchingGame.STATE_NORMAL
        self.take_step = False if not PLAY_SELF else True
        self.shutdown = False

        self.settings = self.__load_settings(level)

        self.n_obstacles = self.settings['n_obstacles']

        self.n_orbs_collected = 0
        self.n_bonus_orbs_collected = 0
        self.ticks = 0
        self.size = self.width, self.height = self.settings['screen_resolution']
        self.spawn_dist_obs_obs = self.settings['spawn_distance_ratios']['obstacle-obstacle']
        self.spawn_dist_obs_orb = self.settings['spawn_distance_ratios']['obstacle-orb']
        self.spawn_dist_obs_robot = self.settings['spawn_distance_ratios']['obstacle-robot']
        self.spawn_dist_robot_orb = self.settings['spawn_distance_ratios']['robot-orb']
        self.spawn_dist_orb_orb = self.settings['spawn_distance_ratios']['orb-orb']

        self.collided_obstacles = []

    def on_init(self):
        pygame.init()

        if HEADLESS:
            self._display_surface = pygame.display.set_mode(self.size, pygame.NOFRAME, 24)
        else:
            self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self._running = False
        self.floor = Floor(self.width, self.height)
        self.obstacles = self._init_obstacles(self.settings['n_obstacles'])
        self.robot = self._spawn_robot()
        self._init_orbs()

        self._running = True

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            while self.take_step:
                self.step()

        if self.shutdown:
            self.on_cleanup()

    def step(self, robot_action=None):
        if not PLAY_SELF: self.take_step = False
        self.ticks += 1
        if robot_action is None and PLAY_SELF:
            for event in pygame.event.get():
                self.on_event(event)
        else:
            self.robot.update(robot_action)

        self.on_loop()
        self.on_render()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if PLAY_SELF:
            if event.type == pygame.KEYDOWN:
                robot_action = self.determine_robot_action(event.key)
                self.robot.update(robot_action)

            if event.type == pygame.KEYUP:
                self.robot.update(Robot.ACTION_NOTHING)

    def handle_pressed_keys(self, pressed_keys):
        obstacle = self.obstacles[0]
        if pressed_keys[K_UP]:
            obstacle.__move__(obstacle.position.x, obstacle.position.y - 1)
        elif pressed_keys[K_DOWN]:
            obstacle.__move__(obstacle.position.x, obstacle.position.y + 1)
        elif pressed_keys[K_LEFT]:
            obstacle.__move__(obstacle.position.x - 1, obstacle.position.y)
        elif pressed_keys[K_RIGHT]:
            obstacle.__move__(obstacle.position.x + 1, obstacle.position.y)

    def on_loop(self):
        caught_orb = spritecollideany(self.robot, self.orbs)
        if caught_orb is not None:
            self.n_orbs_collected += 1
            if type(caught_orb) == BonusOrb:
                self.n_bonus_orbs_collected += 1

            caught_orb.kill()

            if PLAY_SELF and self.normal_orb_is_caught():
                self.reset()

        colliding_obstacle = spritecollideany(self.robot, self.obstacles)
        if colliding_obstacle is not None:
            if colliding_obstacle not in self.collided_obstacles:
                self.collided_obstacles.append(colliding_obstacle)
            self.robot.reset_to_prev_position()

        if self.n_obstacles > 1:
            if self.state is not OrbCatchingGame.STATE_BONUS and len(self.collided_obstacles) == self.n_obstacles:
                self.go_in_bonus_mode()

    def on_render(self):
        self.floor.draw(self._display_surface)
        self._draw_obstacles(self._display_surface)
        self._draw_orbs(self._display_surface)
        self.robot.draw(self._display_surface)

        pygame.display.flip()

    def reset(self):
        self._running = False
        self.state = OrbCatchingGame.STATE_NORMAL
        self.obstacles = self._init_obstacles(self.settings['n_obstacles'])
        self._init_orbs()
        self.collided_obstacles = []
        self.n_bonus_orbs_collected = 0
        self.n_orbs_collected = 0

        self._running = True

    def on_cleanup(self):
        pygame.quit()

    def _init_obstacles(self, n):
        if hasattr(self, 'obstacles') and self.obstacles is not None:
            [obstacle.kill() for obstacle in self.obstacles]

        obstacles = pygame.sprite.Group()
        for n_obstacle in range(n):
            obstacle_width, obstacle_height = self.settings['obstacle_size']

            while True:
                x, y = random.randint(0, self.floor.width - obstacle_width), random.randint(0,
                                                                                            self.floor.height - obstacle_height)
                obstacle = Obstacle(x, y, self.settings['obstacle_size'])

                if not spritecollideany(obstacle, obstacles, collide_rect_ratio(self.spawn_dist_obs_obs)):
                    if hasattr(self, 'robot') and self.robot is not None:
                        if not collide_rect_ratio(self.spawn_dist_obs_robot)(obstacle, self.robot):
                            break
                    else:
                        break

            obstacles.add(obstacle)

        return obstacles

    def _init_orbs(self):
        if hasattr(self, 'orbs') and self.orbs is not None:
            [orb.kill() for orb in self.orbs]

        self.orbs = pygame.sprite.Group()
        self.spawn_new_orb_randomly()

    def _draw_obstacles(self, display):
        [display.blit(obstacle.surf, obstacle.rect) for obstacle in self.obstacles]

    def _draw_orbs(self, display):
        [display.blit(orb.surf, orb.rect) for orb in self.orbs]

    def determine_robot_action(self, key):
        if key == K_DOWN:
            return Robot.ACTION_DOWN
        elif key == K_UP:
            return Robot.ACTION_UP
        elif key == K_RIGHT:
            return Robot.ACTION_RIGHT
        elif key == K_LEFT:
            return Robot.ACTION_LEFT

    def spawn_new_orb_randomly(self):
        while True:
            # do not spawn orbs on top of robot or obstacles or outside the floor
            orb_width, orb_height = self.settings['orb_size']
            x, y = random.randint(0, self.floor.width - orb_width), random.randint(0, self.floor.height - orb_height)

            new_orb = Orb(x, y, self)
            if self.state == OrbCatchingGame.STATE_BONUS:
                new_orb = BonusOrb(x, y, self)

            if not spritecollideany(new_orb, self.obstacles, collide_rect_ratio(self.spawn_dist_obs_orb)) and \
                    not collide_rect_ratio(self.spawn_dist_robot_orb)(new_orb, self.robot) and \
                    not spritecollideany(new_orb, self.orbs, collide_rect_ratio(self.spawn_dist_orb_orb)):
                break

        self.orbs.add(new_orb)

    def _spawn_robot(self):
        while True:
            robot_w, robot_h = self.settings['robot_size']
            x, y = random.randint(0, self.floor.width - robot_w), random.randint(0, self.floor.height - robot_h)
            robot = Robot(x, y, self.floor, self)

            if not spritecollideany(robot, self.obstacles):
                break

        return robot

    def go_in_bonus_mode(self):
        self.state = OrbCatchingGame.STATE_BONUS
        [self.spawn_new_orb_randomly() for n in range(self.settings['n_bonus_orbs'])]

    def get_last_frame(self):
        img_as_array = pygame.surfarray.array3d(pygame.display.get_surface())

        # DEBUG
        # import PIL.Image
        # import PIL
        # img = PIL.Image.fromarray(img_as_array, 'RGB')
        # img.show()
        return img_as_array

    def normal_orb_is_caught(self):
        for orb in self.orbs:
            if type(orb) == Orb:
                return False

        return True

    def respawn_robot(self):
        if self.robot is not None:
            self.robot.kill()

        self.robot = self._spawn_robot()

    @property
    def normal_orb(self):
        for orb in self.orbs:
            if type(orb) == Orb:
                return orb

        return None

    def __load_settings(self, level):
        assert level in (1, 2, 3)
        settings = files.settings()
        settings['level1']['screen_resolution'] = tuple(settings['level1']['screen_resolution'])
        settings['level2']['screen_resolution'] = tuple(settings['level2']['screen_resolution'])
        settings['level3']['screen_resolution'] = tuple(settings['level3']['screen_resolution'])

        return settings['level{}'.format(level)]


if __name__ == "__main__":
    game = OrbCatchingGame()
    game.on_execute()
