import pygame
import random
import os

# we set up the screen size and the fps
screen_width = 1040
screen_height = 704
fps = 60

# here we initialise the windows
pygame.init()
pygame.mixer.init() # we will use this for sound
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('text !!')
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (  0,   0,   0)
green = (0,   255,   0)

# we set up the assests
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,'image')
snd_folder = os.path.join(game_folder,'sound')

font_name = pygame.font.match_font('Arial')
# we create a function to draw text
def text(surface,text,size,x,y):
    font = pygame.font.SysFont(font_name,size)
    text_surface = font.render(text,True,white)
    text_rect = text_surface.get_rect()
    text_rect.midtop =(x,y)
    surface.blit(text_surface,text_rect)


# we create the class with the player sprite
def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img,img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(rocket,(50,38))
     #   self.image.set_colorkey(black)
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
      #  self.speedx = 8
        if event.type == pygame.KEYDOWN:                            #    keystate = pygame.key.get_pressed()
                                                                    #    if keystate[pygame.K_LEFT]:

            if event.key == pygame.K_LEFT:
                self.rect.x -= 4
            if event.key == pygame.K_RIGHT:
                self.rect.x += 4
            if event.key == pygame.K_UP: 
                self.rect.y -= 4 
            if event.key == pygame.K_DOWN: 
                self.rect.y += 4




            # check whether we are hidden
            if self.hidden and pygame.time.get_ticks() -self.hide_timer > 1000:
                self.hidden = False
                self.rect.center =(screen_width/2, screen_height-48)

    # we will use this to shoot bullets
    def shoot(self):
        bullet = Bullet(self.rect.x,self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

    # we will use this to hide the player temproarily
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (screen_width/2,screen_height + 200)
# we create the class for moving enemies 
class Mobs(pygame.sprite.Sprite):
    def __init__(self): # we initialise all the variables
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(meteor,(13,32))
    #   self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.9/2)
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.x = random.randrange(0,screen_width-8)
        self.rect.y = random.randrange(100,screen_height-400)
        self.speedy = random.randrange(1,4)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    def rotation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot += (self.rot_speed)%360
            new_img = pygame.transform.rotate(self.image_orig,self.rot)
            old_center = self.rect.center
            self.image = new_img
            self.rect =self.image.get_rect()
            self.rect.center = old_center
    def update(self): # this will be used to move the object
        self.rotation()
        self.rect.y += self.speedy
        if self.rect.y > screen_height:
            self.rect.x = random.randrange(0,screen_width-500)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,4)


# we create the bullet sprite here
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser,(10,20))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.bottom = y
        self.rect.centerx = x+24
        self.speedy = -4

    def update(self):
        self.rect.y + self.speedy
        if self.rect.y < 0:
            self.kill()
        pygame.display.update()

# we create this class for explosions
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[size][0]
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
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else :
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# this will help us to draw sheild bar
def draw_shield_bar(surf,x,y,pct):
    if pct<0:
        pct =0
    bar_length =100
    bar_height =10
    fill =(pct/100)*bar_length
    outline_rect = pygame.Rect(x,y,bar_length,bar_height)
    fill_rect = pygame.Rect(x,y,fill,bar_height)
    pygame.draw.rect(surf,green,fill_rect)
    pygame.draw.rect(surf,white,outline_rect,2)


# we load the graphics here 
background = pygame.image.load('I+S/indoor.png')
background_rect = background.get_rect()
rocket = pygame.image.load('I+S/gus 2.png')
rocket_miniature = pygame.transform.scale(rocket,(25,15))
rocket_miniature.set_colorkey(black)
meteor = pygame.image.load('I+S/broom.png')
laser = pygame.image.load('I+S/attack.png')
explosion_anim ={}
explosion_anim['lg']= []
explosion_anim['sm']=[]
explosion_anim['player']=[]
for i in range(0,8):
    filename = pygame.image.load('I+S/bottle.png')
    filename1 = pygame.image.load('I+S/bottle.png')
    img1 = (filename1).convert()
    img = (filename).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    img1.set_colorkey(black)
    explosion_anim['player'].append(img1)
# we creare the function for sprites so that we can manage all the sprites

player = Player()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
# load all the sound
shoot_sound = pygame.mixer.Sound('I+S/swoosh.wav')
explosion_sound = pygame.mixer.Sound('I+S/Cat_Meow.wav')
pygame.mixer.music.load('I+S/gameLoops.mp3')
pygame.mixer.music.set_volume(1)
# as we need multiple eneimies we will use a for loop
for i in range(8):
    m = Mobs()
    mobs.add(m)
    all_sprites.add(m)
    

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
                player.shoot()
                
    
    # update each sprite

    all_sprites.update()
    # check whether bullet hit
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    if hits:
        explosion_sound.play()
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        m = Mobs()
        all_sprites.add(m)
        mobs.add(m)

    
        

    # here we see whether it will hit or not
    hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        expl1 = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl1)
        m = Mobs()
        all_sprites.add(m)
        mobs.add(m)
        player.shield -= 10
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.player_lives -= 1
            player.shield = 100

        if hits == False:
            pygame.sprite.Group.clear() 
            hits = bullets.pygame.sprite.empty()
        #   bullets.add()


            

    if player.player_lives == 0 and not death_explosion.alive():
        running = False

    
    # here we fill the background

    screen.fill(black)
    # we darw the background here (image,size)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    text(screen,str(score),18,screen_width/2,10)
    draw_shield_bar(screen,5,5,player.shield)
    draw_lives(screen,screen_width-100,5,player.player_lives,rocket_miniature)
    # we will update the screen

    pygame.display.update()

    
pygame.quit()

