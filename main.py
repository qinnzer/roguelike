import os
import sys

import pygame
import random

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Border(pygame.sprite.Sprite):
    def __init__(self, all_sprites, x, y, x1, y1):
        super().__init__(all_sprites)
        if y == y1:
            self.image = pygame.Surface([x1 - x, 5])
            self.rect = pygame.Rect(x, y, 1, y1 - y)
        else:
            self.image = pygame.Surface([5, y1 - y])
            self.rect = pygame.Rect(x, y, x1 - x, 1)
        self.mask = pygame.mask.from_surface(self.image)


class Hero(pygame.sprite.Sprite):
    def __init__(self, all_sprites, photo):
        super().__init__(all_sprites)
        self.image = load_image(photo)
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 250
        self.rect.y = 250


class Player(Hero):
    def __init__(self, all_sprites, v, photo):
        super().__init__(all_sprites, photo)
        self.v = v

    def update(self):
        flag_w = False if pygame.sprite.collide_mask(self, border1) else True
        flag_a = False if pygame.sprite.collide_mask(self, border3) else True
        flag_s = False if pygame.sprite.collide_mask(self, border2) else True
        flag_d = False if pygame.sprite.collide_mask(self, border4) else True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and flag_w:
            self.rect = self.rect.move(0, -self.v)
        if keys[pygame.K_s] and flag_s:
            self.rect = self.rect.move(0, self.v)
        if keys[pygame.K_a] and flag_a:
            self.rect = self.rect.move(-self.v, 0)
        if keys[pygame.K_d] and flag_d:
            self.rect = self.rect.move(self.v, 0)
        if pygame.sprite.collide_mask(self, evil):
            pygame.display.set_caption('Конец игры!')


class Evil(Hero):
    def __init__(self, all_sprites, v, photo):
        super().__init__(all_sprites, photo)
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(50, 50, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)
        self.mask = pygame.mask.from_surface(self.image)
        self.v = v

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.collide_mask(self, border1) or pygame.sprite.collide_mask(self, border2):
            self.vy = -self.vy
        if pygame.sprite.collide_mask(self, border3) or pygame.sprite.collide_mask(self, border4):
            self.vx = -self.vx


if __name__ == '__main__':
    fps = 60
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    clock = pygame.time.Clock()

    border1 = Border(all_sprites, 5, 5, width - 5, 5)
    border2 = Border(all_sprites, 5, height - 10, width - 5, height - 10)
    border3 = Border(all_sprites, 5, 5, 5, height - 5)
    border4 = Border(all_sprites, width - 10, 5, width - 10, height - 5)
    Player(all_sprites, 2, "hero.png")
    evil = Evil(all_sprites, 2, "evil.png")

    running = True
    while running:
        screen.fill("White")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
