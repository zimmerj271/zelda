import pygame
from pygame.sprite import Group
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: list[Group], obstacle_sprites: Group) -> None:
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        # hitbox defines the rectangle that will be used for collisions to allow some overlap with obstacles
        self.hitbox = self.rect.inflate(0, -26)

    def input(self) -> None:
        """
        Set direction of vector direction when pressing
        directional keys.
        :return: None
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed: int) -> None:
        """
        Update image rectangle location based on direction
        vector and input speed.
        :param speed: int value that specifies speed of player
        :return: None
        """
        # Normalize the vector to length 1 to ensure
        # player does not move faster when moving
        # diagonally
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center  #  Have self.rect follow self.hitbox


    def collision(self, direction: str):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self) -> None:
        self.input()
        self.move(self.speed)
