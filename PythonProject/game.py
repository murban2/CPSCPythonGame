import random
import sys
import pygame
from pygame import key
from pygame.sprite import Sprite, Group, spritecollideany
import settings


class Viewport:
    """
    This class is in charge of managing the user screen for level one.
    """
    def __init__(self):
        self.left = 0


    def update(self, sprite):
        if sprite.world_rect.left < 515:
            self.left = 0
        if sprite.world_rect.left > 515:
            self.left = sprite.world_rect.left - 515
        if sprite.world_rect.left > 2800:
            self.left = 2800 - 515


    def compute_rect(self, group, dx = 0):

        for sprite in group:
            sprite.rect = sprite.world_rect.move(-self.left + dx, 0)

    def draw_group(self, group, surface):

        for sprite in group:
            self.compute_rect(group)
            group.draw(surface)
            if not isinstance(sprite, BackgroundLevelOne) and not isinstance(sprite, FrontgroundLevelOne) or not isinstance(sprite, Rock):
                sprite.update_inset()


        for sprite in group:
            if isinstance(sprite, BackgroundLevelOne) or isinstance(sprite, FrontgroundLevelOne):
                self.compute_rect(group, settings.WORLD_WIDTH)
                group.draw(surface)



class ViewportTwo:
    """
        This class is in charge of managing the user screen for level two.
    """
    def __init__(self):
        self.left = 0


    def update(self, sprite):
        """
         updates the screen position
        Args:
            sprite: the player sprite
        """
        if sprite.world_rect.left < 515:
            self.left = 0
        if sprite.world_rect.left > 515:
            self.left = sprite.world_rect.left - 515
        if sprite.world_rect.left > 2300:
            self.left = 2300 - 515


    def compute_rect(self, group, dx = 0):
        """
        computes screen location of sprites
        Args:
            group: sprites to position
            dx: offset
        """
        for sprite in group:
            sprite.rect = sprite.world_rect.move(-self.left + dx, 0)

    def draw_group(self, group, surface):
        """
        draw sprites to screen
        Args:
            group: sprites to draw
            surface: surface to draw to
        """
        for sprite in group:
            self.compute_rect(group)
            group.draw(surface)
            if not isinstance(sprite, BackgroundLevelTwo):
                sprite.update_inset()
        for sprite in group:
            if isinstance(sprite, BackgroundLevelTwo) or isinstance(sprite, FrontgroundLevelTwo) :
                self.compute_rect(group, settings.WORLD_TWO_WIDTH)
                group.draw(surface)



class KnightEnemy(Sprite):
    """
    class for KnightEnemy sprite
    """
    def __init__(self, x, *groups):
        super().__init__(*groups)

        self.walk_sprite = [pygame.image.load("assets/enemies/knight_animate/knight_walk_frame1.png"),
                            pygame.image.load("assets/enemies/knight_animate/knight_walk_frame2.png"),
                            pygame.image.load("assets/enemies/knight_animate/knight_walk_frame3.png"),
                            pygame.image.load("assets/enemies/knight_animate/knight_walk_frame4.png"),
                            pygame.image.load("assets/enemies/knight_animate/knight_walk_frame5.png"),
                            pygame.image.load("assets/enemies/knight_animate/knight_walk_frame6.png"),
                            pygame.image.load("assets/enemies/knight_animate/knight_walk_frame7.png"),
                            pygame.image.load("assets/enemies/knight_animate/knight_walk_frame8.png")]

        self.flip = True
        self.current_frame = 0
        self.image = self.walk_sprite[self.current_frame].convert_alpha()

        self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale_by(self.image, 2)

        self.rect = self.image.get_rect()
        self.world_rect = self.image.get_rect().move(x, 480)
        self.world_inset_rect = None

    def update_inset(self):
        """
        creates hitbox inset for more accurate collisions.
        """
        self.world_inset_rect = self.world_rect.inflate(-160, -0)
        self.rect = self.world_inset_rect

    def update(self):
        """
        updates position of knight sprites
        """
        self.world_rect.x -= settings.KNIGHT_SPEED
        self.update_inset()




    def animate_walk(self):
        """
        updates walking animation for knight sprites
        """
        self.current_frame += 1
        if self.current_frame >= len(self.walk_sprite):
            self.current_frame = 0
        self.image = self.walk_sprite[self.current_frame].convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale_by(self.image, 2)


class Attack(Sprite):
    """
    hitbox used for user attacks.
    """
    def __init__(self, enemies, player, viewport, *groups):
        super().__init__(*groups)
        self.enemies = enemies
        self.player = player
        self.attack_group = Group()

        self.viewport = viewport

        self.image = pygame.Surface((55, 32))
        self.image.set_colorkey((0,0,0))

        self.rect = self.image.get_rect()
        self.world_rect = self.rect
        self.attack_group.add()

    def update(self):
        """
        placing the attack hitbox on the correct side of the player
        """
        if self.player.flip:
            self.world_rect.x = self.player.rect.x + 80
        else:
            self.world_rect.x = self.player.rect.x - 90
        self.world_rect.y = self.player.rect.y + 120
        self.rect = self.world_rect

    def update_inset(self):
        """
        required method override. method is unneeded
        """
        pass

class Bird(Sprite):
    """class for bird sprites from level one."""
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.fly_sprite = [pygame.image.load("assets/creature/bird/bird_1.png"),
                           pygame.image.load("assets/creature/bird/bird_2.png"),
                           pygame.image.load("assets/creature/bird/bird_3.png"),
                           pygame.image.load("assets/creature/bird/bird_4.png"),
                           pygame.image.load("assets/creature/bird/bird_5.png"),
                           pygame.image.load("assets/creature/bird/bird_6.png"),
                           pygame.image.load("assets/creature/bird/bird_7.png"),
                           pygame.image.load("assets/creature/bird/bird_8.png")]

        self.current_frame = 0
        self.image = self.fly_sprite[self.current_frame]
        self.flip = True
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect().move(x, y)
        self.world_rect = self.rect

        self.height_sign = -1

    def update(self):
        """
        updates position of the birds and the image.
        """
        if self.world_rect.x > 2000:
            self.flip = False
        elif self.world_rect.x < 200:
            self.flip = True

        if self.flip:
            self.world_rect.x += settings.BIRD_HORIZONTAL_SPEED
            self.world_rect.y += settings.BIRD_VERTICAL_SPEED * self.height_sign
            self.image = self.fly_sprite[self.current_frame]
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.world_rect.x -= settings.BIRD_HORIZONTAL_SPEED
            self.world_rect.y += settings.BIRD_VERTICAL_SPEED * self.height_sign
            self.image = self.fly_sprite[self.current_frame]

        if self.world_rect.y < 100:
            self.height_sign = 1
        elif self.world_rect.y > 200:
            self.height_sign = -1

        self.fly_animation()

    def update_inset(self):
        pass

    def fly_animation(self):
        """
        changing frame of animation.
        """
        if self.current_frame > 6:
            self.current_frame = 0
        else:
            self.current_frame += 1




class Duck(Sprite):
    """
    class for the ducks on level two.
    """
    def __init__(self, x, screen, *groups):
        super().__init__(*groups)
        self.bounce_sprite = [pygame.image.load("assets/enemies/duck/duck_1.png"),
                              pygame.image.load("assets/enemies/duck/duck_2.png"),
                              pygame.image.load("assets/enemies/duck/duck_3.png"),
                              pygame.image.load("assets/enemies/duck/duck_4.png")]
        self.rotation = 0
        self.screen = screen

        self.flip = True
        self.current_frame = 0
        self.image = self.bounce_sprite[self.current_frame].convert_alpha()

        self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.world_rect = self.image.get_rect().move(x, -100)
        self.world_inset_rect = None


    def update_inset(self):
        """
        inset change for more accurate hitboxes
        """
        self.world_inset_rect = self.world_rect.inflate(-70, -70)
        self.rect = self.world_inset_rect


    def update(self):
        """
        updates position of the ducks.
        """
        self.world_rect.y += settings.DUCK_SPEED
        self.image = pygame.transform.rotate(self.bounce_sprite[self.current_frame], -180)
        self.update_inset()

    def iterate_animation(self):
        """iterates through the frames of the animation"""
        self.current_frame += 1
        if self.current_frame >= len(self.bounce_sprite):
            self.current_frame = 0


class Chest(Sprite):
    """
    class for the chest on level two.
    """
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load("assets/misc/chest_gold.png")
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect()
        self.world_rect = self.image.get_rect().move(2500, 612)
        self.rect = self.world_rect
        self.world_inset_rect = None

    def update_inset(self):
        """inset for more accurate hitboxes"""
        self.world_inset_rect = self.world_rect.inflate(-0, 200)
        self.rect = self.world_inset_rect

    def update(self):
        """required override. calls update inset."""
        self.update_inset()


class Player(Sprite):
    """
    Manages the player sprite
    """
    def __init__(self, viewport, height, *groups):
        super().__init__(*groups)
        self.current_animation = 0
        self.animation_counter = 0
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
        self.world_rect = self.image.get_rect().move(300, height )
        self.world_inset_rect = None

        self.viewport = viewport

        self.update_inset()


    def update_inset(self):
        """ update inset for more accurate hitbox.
        """

        self.world_inset_rect = self.world_rect.inflate(-240, -150)
        self.rect = self.world_inset_rect


    def update(self, keys):
        """
        update position
        Args:
            keys: key pressed by user.
        """
        self.current_animation = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left()
            self.current_animation = 1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right()
            self.current_animation = 1
        if keys[pygame.K_SPACE] and self.current_frame < 13:
            self.current_animation = 2
        self.update_inset()

    def move_left(self):
        """move the player left."""
        self.world_rect.x -= settings.MOVE_SPEED
        if self.world_rect.x < 0:
            self.world_rect.x = 0
        self.flip = False

    def move_right(self):
        """move the player right"""
        self.world_rect.x += settings.MOVE_SPEED
        self.flip = True


    def attack_player_animation(self, enemies):
        """change attack animation frame for player."""
        if self.current_frame > 13:
            self.current_frame = 0
        else:
            self.current_frame += 1

        if 8 > self.current_frame < 11:
            attack = Attack(enemies, self, self.viewport)
            attack.update()


        self.image = self.attack_sprite[self.current_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)


    def walk_player_animation(self):
        """change walk animation frame for player."""
        if self.current_frame > 10:
            self.current_frame = 0
        else:
            self.current_frame += 1
        self.image = self.walk_sprite[self.current_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)




    def idle_player_animation(self):
        """change idle animation frame for player."""
        if self.current_frame > 4:
            self.current_frame = 0
        else:
            self.current_frame += 1
        self.image = self.idle_sprite[self.current_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)


    def get_frame_count(self):
        """return frame count based on current animation running."""

        if self.current_animation == 0:
            return 10
        if self.current_animation == 1:
            return 5
        if self.current_animation == 2:
            return 4

class BackgroundLevelOne(Sprite):
    """class for the background in level one."""
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load('assets/background/level_one/background_main.png').convert()
        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.SCREEN_HEIGHT

    def update_inset(self):
        """required override."""
        pass

class BackgroundLevelTwo(Sprite):
    """class for the background in level two."""
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load('assets/background/level_two/background_snow.png').convert()
        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.SCREEN_HEIGHT

    def update_inset(self):
        """required override."""
        pass

class FrontgroundLevelOne(Sprite):
    """class for the ground in front of the player in level one."""
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load('assets/background/level_one/layer1.png').convert()
        self.image.set_colorkey((0,0,0))

        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.SCREEN_HEIGHT

    def update_inset(self):
        """required override."""
        pass

class FrontgroundLevelTwo(Sprite):
    """class for the ground in front of the player in level two."""
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load('assets/background/level_two/layer1.png').convert_alpha()

        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.SCREEN_HEIGHT

    def update_inset(self):
        """required override."""
        pass

class Rock(Sprite):
    """class for the rock at the start of each level."""
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load('assets/background/level_one/BigRock1.png').convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False)

        self.world_rect = self.image.get_rect().copy()
        self.world_rect.bottom = settings.SCREEN_HEIGHT + 200
        self.world_rect.x = -300

    def update_inset(self):
        """required override."""
        pass


class Game:
    """class for gameloop and game functionality."""
    def __init__(self):

        pygame.font.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption('This is a game.')
        self.viewport = Viewport()

        #level 1 references
        self.attack = 15
        self.player_level_one = Player(self.viewport, 450)
        self.player_one_group = Group()
        self.player_one_group.add(self.player_level_one)
        self.amount_of_enemies = 5
        self.enemy_knights_group = Group()
        for i in range(5):
            self.enemy_knights_group.add(KnightEnemy(1800 + (400 * i)))
        self.attack_group = Group()
        self.static_sprites = Group()
        self.static_sprites.add(BackgroundLevelOne())
        self.single_sprites = Group()
        self.single_sprites.add(Rock())
        self.front_sprites = Group()
        self.front_sprites.add(FrontgroundLevelOne())
        self.bird_sprites = Group()
        for i in range(9):
            self.bird_sprites.add(Bird(random.randint(300, 1900), random.randint(100, 200)))
        self.viewport.update(self.player_level_one)


        #transition references.
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = self.font.render("Level One Completed.", True, (0, 255, 0))
        self.text_rect = self.text_surface.get_rect(center=(660, 200))

        self.button_rect = pygame.Rect(self.text_rect.x + 50, self.text_rect.y + 120, 180, 40)
        self.button_text = self.font.render("Next Level?", True, (0, 255, 0))
        self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)

        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.death_text_surface = self.font.render("You Died.", True, (0, 255, 0))
        self.death_text_rect = self.death_text_surface.get_rect(center=(660, 200))

        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.win_text_surface = self.font.render("You Won!", True, (0, 255, 0))
        self.win_text_rect = self.win_text_surface.get_rect(center=(660, 200))


        # level2 references

        self.viewport_two = ViewportTwo()
        self.attack = 15
        self.player_level_two = Player(self.viewport_two, 520)
        self.player_two_group = Group()
        self.player_two_group.add(self.player_level_two)

        self.duck_group = Group()

        self.single_sprites_two = Group()
        self.single_sprites_two.add(Rock())

        self.chest_group = Group()
        self.chest_group.add(Chest())

        self.background_two_group = Group()
        self.background_two_group.add(BackgroundLevelTwo())

        self.frontground_two_group = Group()
        self.frontground_two_group.add(FrontgroundLevelTwo())

        self.viewport_two.update(self.player_level_two)


        #state references
        self.level_one = True
        self.between_levels = False
        self.level_two = False
        self.won_game = False


    def game_loop(self):
        """
        The main loop the game runs on.
        """

        frame_num_one = 0
        frame_num_two = 0
        clock = pygame.time.Clock()

        while self.level_one:
            self.handle_events()
            self.draw()
            self.update()
            player_frames = self.player_level_one.get_frame_count()
            animation_num = self.player_level_one.current_animation
            pygame.display.flip()
            frame_num_one += 1

            if frame_num_one % player_frames == 0:
                self.player_one_animation(self.player_level_one, animation_num)
            if frame_num_one % 8 == 0:
                for enemy in self.enemy_knights_group:
                    enemy.animate_walk()
            clock.tick(settings.FPS)

        self.draw_result()
        self.between_levels = True
        self.remove_level_one_sprites()


        while self.between_levels:
            self.handle_events()
            pygame.display.flip()
            clock.tick(settings.FPS)


        self.level_two = True

        pygame.display.flip()

        while self.level_two:
            self.handle_events()
            self.draw_two()
            self.update_two()

            player_frames = self.player_level_two.get_frame_count()
            animation_num = self.player_level_two.current_animation
            frame_num_two += 1
            if frame_num_two % player_frames == 0:
                self.player_one_animation(self.player_level_two, animation_num)

            if frame_num_two % 60 == 0:
                self.duck_group.add(Duck(random.randint(700, 2500), self.screen))

            if frame_num_two % 10 == 0:
                for duck in self.duck_group:
                    duck.iterate_animation()


            pygame.display.flip()
            clock.tick(settings.FPS)

        if self.won_game:
            self.win_screen(clock)


    def win_screen(self, clock):
        """
        The win screen for the end of level 2.
        Args:
            clock: the clock object from the game loop.
        """
        while True:
            self.handle_events()

            pygame.draw.rect(self.screen, (100, 0, 0), self.win_text_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.win_text_rect, 3)
            self.screen.blit(self.win_text_surface, self.win_text_rect)
            pygame.display.flip()
            clock.tick(settings.FPS)


    def remove_level_one_sprites(self):
        """removing all level one sprites."""
        for fg in self.front_sprites:
            fg.kill()
        for bg in self.static_sprites:
            bg.kill()
        for enemy in self.enemy_knights_group:
            enemy.kill()
        for player in self.player_one_group:
            player.kill()
            self.player_level_one.kill()



    def draw_result(self):
        """drawing the result from level one (win or loss)."""
        if self.player_one_group:
            pygame.draw.rect(self.screen, (100, 0, 0), self.text_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.text_rect, 3)
            self.screen.blit(self.text_surface, self.text_rect)

            pygame.draw.rect(self.screen, (100, 100, 100), self.button_rect)
            pygame.draw.rect(self.screen, (50, 50, 50), self.button_rect, 3)
            self.screen.blit(self.button_text, self.button_text_rect)
        else:

            pygame.draw.rect(self.screen, (100, 0, 0), self.death_text_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.death_text_rect, 3)
            self.screen.blit(self.death_text_surface, self.death_text_rect)


    def handle_events(self):
        """handling quit event"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and event.mod == pygame.KMOD_LCTRL:
                    pass

            if self.between_levels:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        self.between_levels = False



    def update(self):
        """updating moving models for level one"""
        self.player_one_group.update(key.get_pressed())

        for enemy in self.enemy_knights_group:
            enemy.update()
        for attack in self.attack_group:
            attack.update()
        for bird in self.bird_sprites:
            bird.update()

        self.viewport.update(self.player_level_one)
        self.player_level_one.update_inset()
        self.check_collisions()

        if self.amount_of_enemies <= 0:
            self.level_one = False


    def update_two(self):
        """updating moving models for level 2"""
        self.player_two_group.update(key.get_pressed())

        for duck in self.duck_group:
            if duck.world_rect.y > 700:
                duck.kill()
            else:
                duck.update()

        self.viewport_two.update(self.player_level_two)
        self.player_level_two.update_inset()

        for chest in self.chest_group:
            chest.update()

        self.check_collisions()



    def draw(self):
        """drawing the sprites for level one"""
        self.screen.fill((0, 0, 0))
        self.viewport.draw_group(self.static_sprites, self.screen)
        self.viewport.draw_group(self.single_sprites, self.screen)
        self.viewport.draw_group(self.player_one_group, self.screen)
        self.viewport.draw_group(self.enemy_knights_group, self.screen)
        self.viewport.draw_group(self.bird_sprites, self.screen)

        if self.attack_group:
            self.viewport.draw_group(self.attack_group, self.screen)

        self.viewport.draw_group(self.front_sprites, self.screen)


    def draw_two(self):
        """drawing the sprites for level 2"""
        self.screen.fill((0,0,0))
        self.viewport_two.draw_group(self.background_two_group, self.screen)
        self.viewport_two.draw_group(self.player_two_group, self.screen)
        self.viewport_two.draw_group(self.duck_group, self.screen)
        self.viewport_two.draw_group(self.chest_group, self.screen)
        self.viewport_two.draw_group(self.frontground_two_group, self.screen)
        self.viewport_two.draw_group(self.single_sprites_two, self.screen)

    def check_collision_knight(self, player, enemy):
        """
        getting result of player collision with Knight enemy
        Args:
            player: the player sprite
            enemy: the enemy collided with.

        Returns: true or false.

        """
        return player.world_inset_rect.colliderect(enemy.rect)

    def check_collision_duck(self, player, duck):
        """
        getting result of player collision with duck enemy
        Args:
            player: the player sprite
            duck: the duck collided with.

        Returns: true or false.

        """
        return player.world_inset_rect.colliderect(duck.rect)

    def check_collision_attack(self, enemy, attack):
        """
        getting result of enemy collision with player attack
        Args:
            enemy: the enemy that was struck
            attack: the attack hitbox

        Returns: true or false

        """
        return enemy.world_inset_rect.colliderect(attack.rect)

    def check_collision_chest(self, player, chest):
        """
        getting result of player collision with chest.
        Args:
            player: the player sprite
            chest: the chest collided with.

        Returns: true or false

        """
        return player.world_inset_rect.colliderect(chest.rect)

    def check_collisions(self):
        """checking for collisions between sprites."""
        if self.player_level_one.alive() and \
                (spritecollideany(self.player_level_one, self.enemy_knights_group, self.check_collision_knight)) is not None:
            self.player_level_one.kill()
            self.level_one = False

        if self.player_level_two.alive() and \
                (spritecollideany(self.player_level_two, self.duck_group, self.check_collision_duck)) is not None:
            self.player_level_two.kill()
            self.level_two = False

        if self.player_level_two.alive() and \
                (spritecollideany(self.player_level_two, self.chest_group, self.check_collision_chest)) is not None:
            self.level_two = False
            self.won_game = True

        for enemy in self.enemy_knights_group:
            if (spritecollideany(enemy, self.attack_group, self.check_collision_attack)) is not None:
                enemy.kill()
                self.amount_of_enemies -= 1


    def player_one_animation(self, player,animation_num):
        """
        changing player animation
        Args:
            player: player sprite
            animation_num: the animation number to perform.

        """
        for attack in self.attack_group:
            attack.kill()
        if animation_num == 2 or self.attack < 15:
            if  8 < player.current_frame < 10:
                self.attack_group.add(Attack(self.enemy_knights_group, player, self.viewport))

            self.attack += 1
            player.attack_player_animation(self.enemy_knights_group)
        elif animation_num == 1:
            player.walk_player_animation()
        elif animation_num == 0:
            player.idle_player_animation()


if __name__ == '__main__':
    Game().game_loop()