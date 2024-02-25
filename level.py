import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self) -> None:
        """

        """
        self.player = None
        # get the display surface - get_surface will return the display surface from anywhere in the code
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        # self.visible_sprites = pygame.sprite.Group()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)


    def run(self) -> None:
        """
         Update and draw the game
        :return: None
        """
        # visible_sprites
        # self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    """
    A class to draw the sprites that are visible on the display
    """
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Player) -> None:
        """
        The custom_draw method loops on all the sprites that have been defined and draws
        the sprite onto the display_surface using blit.  The blit method is used, instead of
        Sprite.draw() because it allows the sprite to be dynamically drawn using an offset.
        In this case the offset is meant to replicate a camera that is centered on the
        player's location in the display, while the remaining sprite images are drawn
        with-respect-to the player location.

        Next, the sprites need to be drawn in the y direction to allow the player sprite
        to overlap on top (images that are drawn after will be placed in the z-direction
        on top of the player image).  To do this, in the for loop, sort each sprite by their
        center y coordinate.
        :param player: Player object
        :return: None
        """
        # get the camera position offset, based on player position
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset  # define draw position with camera offset
            self.display_surface.blit(sprite.image, offset_position)
