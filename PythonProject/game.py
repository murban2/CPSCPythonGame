import sys
import pygame
from pygame import key, Surface
from pygame.sprite import Sprite, Group, spritecollideany
import random
import settings


def wrap_world_rect(rect):
    """Modify rect so that it wraps around if its left side is less than zero or greater than the world width"""
    if rect.left < 0:
        rect.left += settings.WORLD_WIDTH
    if rect.left >= settings.WORLD_WIDTH:
        rect.left -= settings.WORLD_WIDTH


class Viewport:
    def __init__(self):
        self.left = 0


    def update(self, sprite):
        self.left = sprite.world_rect.left - 520

        if self.left  < 0:
            self.left += settings.WORLD_WIDTH
        if self.left > settings.WORLD_WIDTH:
            self.left -= settings.WORLD_WIDTH


    def compute_rect(self, group, dx = 0):
        for sprite in group:
            sprite.rect = sprite.world_rect.move(-self.left + dx, 0)


    def draw_group(self, group, surface):
        self.compute_rect(group)
        group.draw(surface)


        self.compute_rect(group, settings.WORLD_WIDTH)
        group.draw(surface)



class KnightEnemy(Sprite):
    def __init__(self, x, y, screen, *groups):
        super().__init__(*groups)
        self.flip = True
        self.image = pygame.image.load("assets/enemies/knight_animate/knight_walk_frame1.png")
        self.rect = self.image.get_rect()

        self.cropped = None
        self.world_rect = self.image.get_rect().move(x, y)
        self.world_inset_rect = None




    def draw(self, screen):
        self.image.set_colorkey((0, 0, 0))
        self.image.fill((255, 0, 0))
        screen.blit(self.image, (self.world_rect.x, self.world_rect.y))


    def update(self, player):
        if player.world_rect.x < self.world_rect.x:
            self.world_rect.move_ip(-settings.ENEMY_SPEED, 0)
        elif player.world_rect.centerx > self.world_rect.centerx:
            self.world_rect.move_ip(settings.ENEMY_SPEED, 0)
        wrap_world_rect(self.world_rect)



class Player(Sprite):
    def __init__(self, viewport, screen, *groups):
        super().__init__(*groups)
        self.current_animation = 0
        self.idle_sprite = [pygame.image.load("assets/player/individualsprites/01_demon_idle/demon_idle_1.png"),
                            pygame.image.load("assets/player/individualsprites/01_demon_idle/demon_idle_2.png"),
                            pygame.image.load("assets/player/individualsprites/01_demon_idle/demon_idle_3.png"),
                            pygame.image.load("assets/player/individualsprites/01_demon_idle/demon_idle_4.png"),
                            pygame.image.load("assets/player/individualsprites/01_demon_idle/demon_idle_5.png"),
                            pygame.image.load("assets/player/individualsprites/01_demon_idle/demon_idle_6.png")]


        self.walk_sprite = [pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_1.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_2.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_3.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_4.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_5.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_6.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_7.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_8.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_9.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_10.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_11.png"),
                            pygame.image.load("assets/player/individualsprites/02_demon_walk/demon_walk_12.png")]

        self.attack_sprite = [pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_1.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_2.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_3.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_4.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_5.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_6.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_7.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_8.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_9.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_10.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_11.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_12.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_13.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_14.png"),
                             pygame.image.load("assets/player/individualsprites/03_demon_cleave/demon_cleave_15.png")]
        self.flip = True
        self.current_frame = 0
        self.image = self.idle_sprite[self.current_frame].convert_alpha()

        self.rect = self.image.get_rect()
        self.world_rect = self.image.get_rect().move(600, 500)
        self.world_inset_rect = None

        self.viewport = viewport

        self.cropped = pygame.Surface((100, 110))
        self.cropped.blit(self.image, (0, 0), (95, 50, 100, 110))
        screen.blit(self.cropped, (self.world_rect.x, self.world_rect.y))

        self.image = self.cropped
        self.update_inset()


    def update_inset(self):
        self.world_inset_rect = self.world_rect.inflate(-100, -110)


    def update(self, keys):
        self.current_animation = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left()
            self.current_animation = 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right()
            self.current_animation = 1
        if keys[pygame.K_SPACE]:
            self.current_animation = 2


        wrap_world_rect(self.world_rect)


        self.rect.x = self.world_rect.x - self.viewport.left
        self.rect.y = self.world_rect.y




    def move_left(self):
        self.world_rect.left -= settings.MOVE_SPEED
        self.update_inset()
        self.flip = False


    def move_right(self):
        self.world_rect.right += settings.MOVE_SPEED
        self.update_inset()
        self.flip = True


    def attack_player_animation(self, screen):
        if self.current_frame > 13:
            self.current_frame = 0
        else:
            self.current_frame += 1
        self.image = self.walk_sprite[self.current_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

        self.cropped = pygame.Surface((100, 110))
        self.cropped.blit(self.image, (0, 0), (95, 50, 100, 110))
        screen.blit(self.cropped, (self.world_rect.x, self.world_rect.y))

        self.image = self.cropped

        self.image.fill((255, 0, 0))





    def walk_player_animation(self, screen):
        if self.current_frame > 10:
            self.current_frame = 0
        else:
            self.current_frame += 1
        self.image = self.walk_sprite[self.current_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

        self.cropped = pygame.Surface((100, 110))
        self.cropped.blit(self.image, (0, 0), (95, 50, 100, 110))
        screen.blit(self.cropped, (self.world_rect.x, self.world_rect.y))

        self.image = self.cropped

        self.image.fill((255, 0, 0))



    def idle_player_animation(self, screen):
        if self.current_frame > 4:
            self.current_frame = 0
        else:
            self.current_frame += 1
        self.image = self.idle_sprite[self.current_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

        self.cropped = pygame.Surface((100, 110))
        self.cropped.blit(self.image, (0, 0), (95, 50, 100, 110))

        screen.blit(self.cropped, (self.world_rect.x, self.world_rect.y))

        self.image = self.cropped

        self.image.fill((255, 0, 0))




    def get_frame_count(self):

        if self.current_animation == 0:
            return 10
        if self.current_animation == 1:
            return 5
        if self.current_animation == 2:
            return 4



class Background(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load('assets/background/background_main.png').convert()

        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.SCREEN_HEIGHT


class Frontground(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load('assets/background/layer1.png').convert()
        self.image.set_colorkey((0,0,0))

        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.SCREEN_HEIGHT


class Game:
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption('This is a game.')
        self.viewport = Viewport()
        self.player = Player(self.viewport, self.screen)

        self.player_group = Group()
        self.player_group.add(self.player)
        self.attack = 15


        self.enemies_group = Group()
        for i in range(5):
            self.enemies_group.add(KnightEnemy(random.randrange(1000, settings.WORLD_WIDTH), 560, self.screen))


        self.static_sprites = Group()
        self.static_sprites.add(Background())

        self.front_sprites = Group()
        self.front_sprites.add(Frontground())


        self.viewport.update(self.player)


    def game_loop(self):
        running = True
        player_frame_num = 0
        clock = pygame.time.Clock()

        while running:
            self.handle_events()
            self.draw()
            self.update()
            player_frames = self.player.get_frame_count()
            animation_num = self.player.current_animation
            pygame.display.flip()
            player_frame_num += 1

            if player_frame_num % player_frames == 0:
                self.player_animation(animation_num)
            clock.tick(settings.FPS)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and event.mod == pygame.KMOD_LCTRL:
                    pass


    def update(self):
        self.player_group.update(key.get_pressed())
        self.viewport.update(self.player)

        for enemy in self.enemies_group.sprites():
            enemy.update(self.player)

        self.check_collisions()

    def check_collision(self, player, enemy):
        return player.world_inset_rect.colliderect(enemy.world_rect)

    def check_collisions(self):
        if self.player.alive() and \
                (collided_with := spritecollideany(self.player, self.enemies_group, self.check_collision)) is not None:
            self.player.kill()




    def draw(self):
        self.screen.fill((0, 0, 0))
        self.viewport.draw_group(self.static_sprites, self.screen)
        self.viewport.draw_group(self.player_group, self.screen)

        for enemy in self.enemies_group.sprites():
            enemy.draw(self.screen)

        self.viewport.draw_group(self.front_sprites, self.screen)

    def player_animation(self, animation_num):
        if animation_num == 2 or self.attack < 15:
            self.attack += 1
            self.player.attack_player_animation(self.screen)
        elif animation_num == 1:
            self.player.walk_player_animation(self.screen)
        elif animation_num == 0:
            self.player.idle_player_animation(self.screen)

if __name__ == '__main__':
    Game().game_loop()