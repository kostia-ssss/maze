import pygame
pygame.init()
from map1 import *

FPS = 60
clock = pygame.time.Clock()

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w , wind_h))
pygame.display.set_caption("MAZE")

background = pygame.image.load("images/bg.jfif")
background = pygame.transform.scale(background, (wind_w , wind_h))

pygame.mixer.music.load("sound.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

class Sprite:
    def __init__(self , x , y , w , h, img):
        self.img = img
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(self.img , (w, h))
    
    def draw(self):
        window.blit(self.img , (self.rect.x, self.rect.y))
        
class Player(Sprite):
    def __init__(self , x , y , w , h , img , speed):
        super().__init__(x, y, w, h, img)
        self.speed = speed
    
    def move(self , walls):
        keys = pygame.key.get_pressed()
        orig_pos = self.rect.copy()
        if keys[pygame.K_w]:
            if self.rect.y > 0:
                self.rect.y -= self.speed
        if keys[pygame.K_s]:
            if self.rect.bottom < wind_h:
                self.rect.y += self.speed
        if keys[pygame.K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[pygame.K_d]:
            if self.rect.right < wind_w:
                self.rect.x += self.speed
        
        for wall in walls:    
            if self.rect.colliderect(wall.rect):
                self.rect = orig_pos

class Enemy(Sprite):
    def __init__(self , x , y , w , h , img , speed):
        super().__init__(x, y, w, h, img)
        self.speed = speed
    
    def move(self):
        pass

blocks = []
block_size = 25

block_x = 0
block_y = 0
block_img = pygame.image.load("images/wall.png")

def otladka():
    print(len(blocks))

for row in lvl1:
    for tile in row:
        if tile == "1":
            blocks.append(Sprite(block_x, block_y, block_size, block_size, block_img))
        block_x += block_size
    block_x = 0
    block_y += block_size

player = Player(35, 50, 20, 20, pygame.image.load("images/steve.png"), 3)

otladka()

game = True
while game:
    window.blit(background, (0, 0))
    
    for b in blocks:
        b.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    
    player.draw()
    player.move(blocks)
    
    pygame.display.update()
    clock.tick(FPS)
    