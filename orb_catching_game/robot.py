import pygame

from orb_catching_game.utilities import files
from orb_catching_game.utilities import color_constants


class Robot(pygame.sprite.Sprite):
    ACTION_NOTHING = -1
    ACTION_UP = 0
    ACTION_DOWN = 1
    ACTION_LEFT = 2
    ACTION_RIGHT = 3

    ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

    class Direction:
        EAST = 0
        SOUTH = 90
        WEST = 180
        NORTH = 270

        @staticmethod
        def rotation(from_direction, to_direction):
            return from_direction - to_direction

    DEFAULT_DIRECTION = Direction.NORTH

    def __init__(self, x, y, floor, game, color=color_constants.GREEN) -> None:
        super(Robot, self).__init__()
        self.floor = floor
        self.color = color
        self.speed = game.settings['robot_speed']
        self.look_at = Robot.DEFAULT_DIRECTION

        self.surf = pygame.Surface(game.settings['robot_size'])

        self.image = pygame.image.load(files.get_resource('triangle.png')).convert()
        self.image = pygame.transform.scale(self.image, game.settings['robot_size'])

        self.rect = self.image.get_rect()
        self.rect = self.surf.get_rect(topleft=(y, x))

        self._prev_rect = self.rect.copy()
        self.action = Robot.ACTION_NOTHING

    @property
    def position(self):
        return self.rect.x, self.rect.y

    def reset_to_prev_position(self):
        self.rect = self._prev_rect.copy()

    def update(self, action):
        self._prev_rect = self.rect.copy()

        self.action = action

        if action == Robot.ACTION_NOTHING:
            return
        elif action == Robot.ACTION_DOWN:
            self.rect.move_ip(0, self.speed)
        elif action == Robot.ACTION_UP:
            self.rect.move_ip(0, -self.speed)
        elif action == Robot.ACTION_LEFT:
            self.rect.move_ip(-self.speed, 0)
        elif action == Robot.ACTION_RIGHT:
            self.rect.move_ip(self.speed, 0)

        # Keep robot on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.floor.width:
            self.rect.right = self.floor.width
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= self.floor.height:
            self.rect.bottom = self.floor.height

    def draw(self, display):
        new_look_at = self.look_at
        if self.action == Robot.ACTION_RIGHT:
            new_look_at = Robot.Direction.EAST
        elif self.action == Robot.ACTION_LEFT:
            new_look_at = Robot.Direction.WEST
        elif self.action == Robot.ACTION_UP:
            new_look_at = Robot.Direction.NORTH
        elif self.action == Robot.ACTION_DOWN:
            new_look_at = Robot.Direction.SOUTH

        self.look_at = new_look_at
        if self.look_at == Robot.Direction.EAST:
            triangle_coordinates = [self.surf.get_rect().topleft, self.surf.get_rect().midright,
                                    self.surf.get_rect().bottomleft]
        elif self.look_at == Robot.Direction.WEST:
            triangle_coordinates = [self.surf.get_rect().midleft, self.surf.get_rect().topright,
                                    self.surf.get_rect().bottomright]
        elif self.look_at == Robot.Direction.NORTH:
            triangle_coordinates = [self.surf.get_rect().midtop, self.surf.get_rect().bottomleft,
                                    self.surf.get_rect().bottomright]
        elif self.look_at == Robot.Direction.SOUTH:
            triangle_coordinates = [self.surf.get_rect().topleft, self.surf.get_rect().midbottom,
                                    self.surf.get_rect().topright]

        self.surf.fill(self.floor.color)
        pygame.draw.polygon(self.surf, self.color, triangle_coordinates)

        # to_rotate = Robot.Direction.rotation(self.look_at, new_look_at)
        # self.look_at = new_look_at
        # if to_rotate != 0:
        #     self.surf = pygame.transform.rotate(self.surf, to_rotate)

        display.blit(self.surf, self.rect)
        # display.blit(self.image, self.position)
