import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: list) -> None:
        """
        Takes the position and sprite group of static obstacles
        and loads the image, assigns the rect to the image, which
        then loads the sprite through inheritance to the Pygame
        Sprite class.
        :param pos: A tuple that is the position on the worldmap.
        Needs to be a multiple of settings.TILESIZE
        :param groups: The sprite group the tile should be assigned to.
        """
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/rock.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  # shrink y of self.rect by 5 pixels on each side.
