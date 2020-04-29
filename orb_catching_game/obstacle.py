import pygame

from orb_catching_game.utilities import color_constants


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, dimension, color=color_constants.WHITESMOKE) -> None:
        super(Obstacle, self).__init__()

        self.dimension = dimension
        self.width, self.height = self.dimension
        self.color = color
        self.touched = False

        self.surf = pygame.Surface(self.dimension)
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(topleft=[x, y])

    def update(self):
        pass

    def draw(self, display):
        pass

    def set_is_touched(self, touched):
        self.touched = touched
        if self.touched:
            self.color = color_constants.BLUE
            self.surf.fill(self.color)
