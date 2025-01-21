import pygame
pygame.init()
from map1 import *
from time import sleep

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
    def __init__(self , x , y , w , h , img1, img2 , speed, dir):
        super().__init__(x, y, w, h, img1)
        self.img_r = self.img
        self.img_l = pygame.transform.scale(img2, (w, h))
        self.speed = speed
        self.dir = dir
    
    def move(self, maze):
        self.rect.x -= self.speed * self.dir
        if any(self.rect.colliderect(obstacle.rect) for obstacle in maze) or self.rect.left <= 0 or self.rect.right >= window.get_width():
            self.dir *= -1
            if self.dir == 1:
                self.img = self.img_l
            if self.dir == -1:
                self.img = self.img_r

blocks = []
Dblocks = []
Coins = []
enemies = []
coins = 0
block_size = 25

block_x = 0
block_y = 0
block_img = pygame.image.load("images/wall.png")
Dblock_img = pygame.image.load("images/danger_wall.png")
Coin_img = pygame.image.load("images/coin.png")
enemy_img1 = pygame.image.load("images/zombie.png")
enemy_img2 = pygame.transform.flip(enemy_img1, True, False)

def otladka():
    print(len(blocks))

for row in lvl1:
    for tile in row:
        if tile == "1":
            blocks.append(Sprite(block_x, block_y, block_size, block_size, block_img))
        elif tile == "2":
            skarb = Sprite(block_x, block_y, 30, 30, pygame.image.load("images/netherite.png"))
        elif tile == "3":
            enemies.append(Enemy(block_x, block_y, 30, 30, enemy_img1, enemy_img2, 3, 1))
        elif tile == "4":
            Dblocks.append(Sprite(block_x, block_y, block_size, block_size, Dblock_img))
        elif tile == "5":
            Coins.append(Sprite(block_x, block_y, block_size, block_size, Coin_img))
        block_x += block_size
    block_x = 0
    block_y += block_size

player = Player(35, 50, 20, 20, pygame.image.load("images/steve.png"), 3)

font = pygame.font.SysFont("Comfortaa" , 50)
font2 = pygame.font.SysFont("Comfortaa" , 20)
font3 = pygame.font.SysFont("Comfortaa" , 35)
win = font.render("You win!", True, (0, 100, 0))
lose = font.render("You lose(", True, (100, 0, 0))
reset = font.render("Press R to reset", True, (0, 0, 0))
coins_t = font3.render(str(coins), True, (0, 0, 0))

game = True
finish = False
while game:
    otladka()
    if not finish:
        window.blit(background, (0, 0))
        
        for b in blocks:
            b.draw()
        
        for b in Dblocks:
            b.draw()
        
        for c in Coins:
            if not player.rect.colliderect(c.rect):    
                c.draw()
            else:
                coins += 1
                Coins.remove(c)
                
        for e in enemies:
            e.draw()
            e.move(blocks)
            
        player.draw()
        skarb.draw()
        player.move(blocks)

        if player.rect.colliderect(skarb.rect):
            window.blit(win, (200, 200))
            window.blit(reset, (200, 250))
            finish = True
        
        if any(player.rect.colliderect(e.rect) for e in enemies):
            window.blit(lose, (200, 200))
            window.blit(reset, (200, 250))
            finish = True
           
        if any(player.rect.colliderect(block.rect) for block in Dblocks):
            player = Player(35, 50, 20, 20, pygame.image.load("images/steve.png"), 3)
        
        coins_t = font3.render(str(coins), True, (0, 0, 0)) 
        window.blit(coins_t, (10, 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and finish == True:
            finish = False
            coins = 0
            player = Player(35, 50, 20, 20, pygame.image.load("images/steve.png"), 3)
    
    pygame.display.update()
    clock.tick(FPS)