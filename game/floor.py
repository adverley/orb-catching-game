import pygame

from utilities import color_constants


class Floor:
    def __init__(self, width, height) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.dimension = (self.width, self.height)

    def draw(self, display):
        pygame.draw.rect(display, color_constants.BLACK, (0, 0, self.width, self.height))