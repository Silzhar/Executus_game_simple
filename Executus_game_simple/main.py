import pygame , sys
import random

pygame.init()

screen_width = 1040
screen_height = 704

pygame.mixer.init() # we will use this for sound
screen = pygame.display.set_mode([screen_width,screen_height])  
pygame.display.set_caption('Executus, the game !!')
clock = pygame.time.Clock()
fps = 60
font_name = pygame.font.match_font('Arial')

white = (255, 255, 255)
black = (  0,   0,   0)
green = (0,   255,   0)


def text(surface,text,size,x,y):  # function to draw text
    font = pygame.font.SysFont(font_name,size)
    textSurface = font.render(text,True,white)
    textRect = textSurface.get_rect()
    textRect.midtop =(x, y)
    surface.blit(textSurface,textRect)


def lives(surf,x,y,lives,img):  # total lives (3) 
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img,img_rect)


def lifeBar(surf,x,y,total):   # life : status / position 
    if total < 0:
        total = 0
    bar_length = 100
    bar_height = 10
    fill =(total/100)*bar_length
    exteriorLifeRect = pygame.Rect(x,y,bar_length,bar_height)
    insideLifeRect = pygame.Rect(x,y,fill,bar_height)
    pygame.draw.rect(surf,green,insideLifeRect)  # life points (green)
    pygame.draw.rect(surf,white,exteriorLifeRect,2) # outer rectangle (whilte) ,life frame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player,(30,28))
        self.rect = self.image.get_rect()
        self.radius = 21
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
        if event.type == pygame.KEYDOWN:                     
            if event.key == pygame.K_LEFT:
                self.rect.x -= 4
            if event.key == pygame.K_RIGHT:
                self.rect.x += 4
            if event.key == pygame.K_UP: 
                self.rect.y -= 4 
            if event.key == pygame.K_DOWN: 
                self.rect.y += 4

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

   
    def knock(self):   # use this to knock bottles
        breaks = Breaks(self.rect.x,self.rect.y)
        all_sprites.add(breaks)
        broken.add(breaks)
        knockSound.play()

    
    def hide(self): # use this to hide the player temproarily (dead)
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (screen_width/2,screen_height + 200)


class Bottle(pygame.sprite.Sprite):
    def __init__(self, position):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bottleOne,(12,30))   
        self.rect = self.image.get_rect()
        self.rect = positions[0]

class Bottle2(pygame.sprite.Sprite):
    def __init__(self, position):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bottleTwo,(12,30))   
        self.rect = self.image.get_rect()
        self.rect = positions[1]


class Breaks(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(attackImage,(10,10))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        self.rect.bottom = y
        self.rect.centerx = x+24
        self.attackImage = -2

    def update(self):
        self.rect.y + self.attackImage
        if self.rect.y < 0:
            self.kill()
       


class Collision(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = collisionFrame[size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(collisionFrame[self.size]):
                self.kill()
            else :
                center = self.rect.center
                self.image = collisionFrame[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# we create the class for moving enemies 
class Brooms(pygame.sprite.Sprite):
    def __init__(self): # we initialise all the variables
        pygame.sprite.Sprite.__init__(self)
        self.imageOrigin = pygame.transform.scale(broom,(13,32))
        self.image = self.imageOrigin.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.9/2)

        self.rect.x = random.randrange(0,screen_width-8)
        self.rect.y = random.randrange(100,screen_height-400)
        self.speedBrooms = random.randrange(1,4)
        self.rot = 0

        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

    def rotation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot += (self.rot_speed)%360
            new_img = pygame.transform.rotate(self.imageOrigin,self.rot)
            oldCenter = self.rect.center
            self.image = new_img
            self.rect =self.image.get_rect()
            self.rect.center = oldCenter

    def update(self): # this will be used to move the object
        self.rotation()
        self.rect.y += self.speedBrooms
        if self.rect.y > screen_height:
            self.rect.x = random.randrange(0,screen_width-500)
            self.rect.y = random.randrange(-100,-40)
            self.speedBrooms = random.randrange(1,4)



# we load the graphics here 
background = pygame.image.load('I+S/indoor.png')
background_rect = background.get_rect()
player = pygame.image.load('I+S/gus 2.png')
playerImageLives = pygame.transform.scale(player,(34,28))

broom = pygame.image.load('I+S/broom.png')
attackImage = pygame.image.load('I+S/attack.png')
bottleOne = pygame.image.load('I+S/bottle.png')
bottleTwo = pygame.image.load('I+S/bottle.png')

collisionFrame ={}
collisionFrame['sm']=[]
collisionFrame['player']=[]

for i in range(0,8):
    breackBottle = pygame.image.load('I+S/breackBottle.png')
    img = (breackBottle) 

    tombstoneOrigin = pygame.image.load('I+S/Tombstone.png')
    tombstone = pygame.transform.scale(tombstoneOrigin,(70,60))
    collisionFrame['player'].append(tombstone)

    img_sm = pygame.transform.scale(breackBottle,(32,32))
    collisionFrame['sm'].append(img_sm)


positions = [(720,602),(868,600)]

Position = positions[0]
position2 = positions[1]

player = Player()


bottle1 = Bottle(Position)
bottle2 = Bottle2(position2)

broken = pygame.sprite.Group()
enemies = pygame.sprite.Group()
totalBottles = pygame.sprite.Group()

bottles = pygame.sprite.Group()
bottles.add(bottle1)
bottles.add(bottle2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
# broken = pygame.sprite.Group()  # necesary ?
all_sprites.add(bottle1)
all_sprites.add(bottle2)



# load all the sound
knockSound = pygame.mixer.Sound('I+S/swoosh.wav')
explosion_sound = pygame.mixer.Sound('I+S/Cat_Meow.wav')
pygame.mixer.music.load('I+S/gameLoops.mp3')
pygame.mixer.music.set_volume(1)


bottleList = []



# as we need multiple eneimies we will use a for loop
for i in range(8):
    brooms = Brooms()
    enemies.add(brooms)
    all_sprites.add(brooms)



score = 0 # this will keep track of the score
pygame.mixer.music.play(loops = -1)
# game loop 
running = True
while running:
    # we tweak the fps here
    clock.tick(fps)

    # we keep track of all the events here
    for event in pygame.event.get():
        # if the user wishes to quit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.knock()


    
    # update each sprite

    all_sprites.update()
    # check whether bullet hit
    hits = pygame.sprite.groupcollide(broken,bottles,True,True)
    if hits:
        explosion_sound.play()
    for hit in hits:
        score += 1
        expl = Collision(hit.rect.center,'sm')
        all_sprites.add(expl)
        all_sprites.add(totalBottles)
    
        

    # here we see whether it will hit or not
    hits = pygame.sprite.spritecollide(player,enemies,True,pygame.sprite.collide_circle)
    for hit in hits:
        expl1 = Collision(hit.rect.center,'sm')
        all_sprites.add(expl1)
        brooms = Brooms()
        all_sprites.add(brooms)
        enemies.add(brooms)
        player.shield -= 50
        if player.shield <= 0:
            death_explosion = Collision(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.player_lives -= 1
            player.shield = 100

        if hits == False:
            pygame.sprite.Group.clear() 
            hits = broken.pygame.sprite.empty()
 

    if player.player_lives == 0 and not death_explosion.alive():
        running = False

    
    # here we fill the background

    # we darw the background here (image,size)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    text(screen,str(score),18,screen_width/2,10)
    lifeBar(screen,5,5,player.shield)
    lives(screen,screen_width-100,5,player.player_lives,playerImageLives)
    # we will update the screen


    pygame.display.update()

pygame.quit()