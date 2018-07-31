import pygame

from orb_catching_game.utilities import color_constants


class Floor:
    def __init__(self, width, height, color=color_constants.BLACK) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.dimension = (self.width, self.height)

        self.color = color

    def draw(self, display):
        pygame.draw.rect(display, self.color, (0, 0, self.width, self.height))