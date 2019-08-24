import pygame , sys
import random

pygame.init()

screen_width = 1040
screen_height = 704

pygame.mixer.init() # we will use this for sound
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('text !!')
clock = pygame.time.Clock()




font_name = pygame.font.match_font('Arial')
# we create a function to draw text
def text(surface,text,size,x,y):
    font = pygame.font.SysFont(font_name,size)
    text_surface = font.render(text,True,(255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop =(x,y)
    surface.blit(text_surface,text_rect)


def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img,img_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player,(50,38))
        self.rect = self.image.get_rect()
        self.radius = 21
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.center = (screen_width/2,screen_height-48)
        self.shield = 100
        self.player_lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    # we will use this class to add movement to the player
    def update(self):
        self.speed = 4
        self.stop = 0
        self.xMove = 0
        self.yMove = 0 
        event = pygame.event.get()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.xMove -= self.speed
            if event.key == pygame.K_RIGHT:
                self.xMove += self.speed
            if event.key == pygame.K_UP:
                self.yMove -= self.speed
            if event.key == pygame.K_DOWN:
                self.yMove += self.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.xMove -= self.stop
            if event.key == pygame.K_RIGHT:
                self.xMove += self.stop
            if event.key == pygame.K_UP:
                self.yMove -= self.stop
            if event.key == pygame.K_DOWN:
                self.yMove += self.stop

        if self.hidden and pygame.time.get_ticks() -self.hide_timer > 1000:
                self.hidden = False
                self.rect.center =(screen_width/2, screen_height-48)

    # we will use this to shoot breaks
    def shoot(self):
        breaks = Breaks(self.rect.x,self.rect.y)
        all_sprites.add(breaks)
        broken.add(breaks)
        shoot_sound.play()

class Breaks(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser,(10,20))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.bottom = y
        self.rect.centerx = x+25
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()
























# we load the graphics here 
background = pygame.image.load('I+S/indoor.png')
background_rect = background.get_rect()
player = pygame.image.load('I+S/gus 2.png')
player_miniature = pygame.transform.scale(player,(25,15))
meteor = pygame.image.load('I+S/broom.png')
laser = pygame.image.load('I+S/broonGame.png')
explosion_anim ={}
explosion_anim['lg']= []
explosion_anim['sm']=[]
explosion_anim['player']=[]




player = Player()
broken = pygame.sprite.Group()
mobs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
broken = pygame.sprite.Group()  # necesary ?

# load all the sound
shoot_sound = pygame.mixer.Sound('I+S/Cat_Meow.wav')
explosion_sound = pygame.mixer.Sound('I+S/Cat_Meow.wav')
pygame.mixer.music.load('I+S/gameLoops.mp3')
pygame.mixer.music.set_volume(1)


pygame.display.update()
pygame.quit()