# Raiden Clone

import pygame
import random
import os
from os import path

Graphics_dir = path.join(path.dirname(__file__), 'Graphics')


WIDTH = 720
HEIGHT = 1080
FPS = 60

# Define Colors

Purple = (100,35,165)
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

# set up asset folders

game_folder = os.path.dirname(__file__)
Graphics_folder = os.path.join(game_folder, "Graphics")

# sprite for the Player Ship
class Ship(pygame.sprite.Sprite):
    def __init__(self): # run this code when this object is created
        pygame.sprite.Sprite.__init__(self) # initializes sprite command
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(Graphics_folder, "1.png")), (60,60)) # what the sprite looks like, .convert() command caused image to break
        self.image.set_colorkey(Black)  # ignores background color of sprite if it exists
        self.rect = self.image.get_rect() # rectangle that encloses the sprite (hit box, etc.)
        self.radius = 25
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0

    def update(self):
        self.speedx = 0 # defines start speed as zero
        self.speedy = 0
        keystate = pygame.key.get_pressed() # define keystate which manages key inputs
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top) # bullet shoot is defined here so that the bullet can use the player defined location to shoot from
        all_sprites.add(bullet)  # make sure to add to all_sprites group
        Bullets.add(bullet  )

class ES1(pygame.sprite.Sprite):    # ES (ENEMY SHIP)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(Graphics_folder, "2.png")), (50, 50))
        self.image.set_colorkey(Black)  # ignores background color of sprite if it exists
        self.rect = self.image.get_rect() # rectangle that encloses the sprite (hit box, etc.)
        self.radius = 20
        self.rect.x = random.randrange(280, 440) # random range starting position in X axis
        self.rect.y = random.randrange(-100, -40) # random range starting position in the Y axis (- is above screen)
        self.speedx = random.randrange(-3, 3) # define x speed
        self.speedy = 5                       # define y speed

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -50 or self.rect.right > WIDTH + 50:  # randomize the spawn location and speed once ES1 leaves the play area
            self.rect.x = random.randrange(280, 440)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-2, 2)
            self.speedy = 7

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0: # remove it if moves off the top of the screen
            self.kill()   # kill command removes sprite from any groups


# Background
class BackgroundImg(pygame.sprite.Sprite):
    def __init__(self):
        self.groups = BG_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.transform.scale(pygame.image.load(path.join(Graphics_dir, "background.png")).convert(),
                                            (720, 2160))
        self.height = 2160
        self.rect = self.image.get_rect()
        # Spawn Background above the screen
        self.rect.top = HEIGHT - self.height
        self.rect.x = 0
        # Scroll speed of background
        self.speed = 10

    def update(self):
        # Spawn new background if the image is at the end
        if self.rect.top == 0:
            BackgroundImg()
        # Kill the background sprite after it goes off screen
        if self.rect.top > HEIGHT:
            self.kill()
        # move screen every frame
        self.rect.top += self.speed

# initialize pygame and create a new window

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KILLOWATT")
clock = pygame.time.Clock()


# Load all game graphics

bullet_img = pygame.image.load(path.join(Graphics_dir, "laser1.png")).convert()
# load all other images here (move the player ones here)

all_sprites = pygame.sprite.Group()
BG_sprite = pygame.sprite.Group()
Enemies = pygame.sprite.Group()
Bullets = pygame.sprite.Group()
Ship = Ship() # make a player object appear
all_sprites.add(Ship)
for i in range(8):
    E = ES1()
    all_sprites.add(E)
    Enemies.add(E)

background = BackgroundImg()
# Game Loop

running = True
while running:
    # Keep the game loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # check for window close
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: # defines shoot event during game
            if event.key == pygame.K_SPACE:
                Ship.shoot()

    # Update game loop
    all_sprites.update() # update sprites
    BG_sprite.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(Enemies, Bullets, True, True)
    for hit in hits:
        E = ES1()
        all_sprites.add(E)
        Enemies.add(E)

    # check to see if player collision occurs
    Collisions = pygame.sprite.spritecollide(Ship, Enemies, False, pygame.sprite.collide_circle) # defines collisions
                # (player sprite, what you want to check hit the sprite, should the enemy the player hit be deleted?)
                # Collide_circle causes it to collide based on circles
    if Collisions:
        running = False

    # Draw / Render
    screen.fill(White)
    # screen.blit(background, background_rect) # copy the background onto the screen
    BG_sprite.draw(screen)
    all_sprites.draw(screen)

    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()