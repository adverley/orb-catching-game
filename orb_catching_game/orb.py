import pygame
from orb_catching_game.utilities import color_constants


class Orb(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super(Orb, self).__init__()
        self.surf = pygame.Surface(game.settings['orb_size'])
        self.surf.fill(color_constants.GOLDENROD)
        self.rect = self.surf.get_rect(topleft=(y, x))

    @property
    def position(self):
        return self.rect.x, self.rect.y


class BonusOrb(Orb):
    def __init__(self, x, y, game):
        super(Orb, self).__init__()
        self.surf = pygame.Surface(game.settings['orb_size'])
        self.surf.fill(color_constants.RED1)
        self.rect = self.surf.get_rect(topleft=(y, x))
