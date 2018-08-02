import pygame

from orb_catching_game.utilities import color_constants


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, dimension, color=color_constants.WHITESMOKE) -> None:
        super(Obstacle, self).__init__()

        self.dimension = dimension
        self.width, self.height = self.dimension

        self.surf = pygame.Surface(self.dimension)
        self.surf.fill(color)
        self.rect = self.surf.get_rect(topleft=[y, x])

    def update(self):
        pass

    def draw(self, display):
        pass
