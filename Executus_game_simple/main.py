import pygame , sys
import random

class Executus(pygame.sprite.Sprite):
    def __init__(self, imagePlayer):
        pygame.sprite.Sprite.__init__(self)
        self.imagePlayer = imagePlayer
        self.rect = self.imagePlayer.get_rect()
        
        self.rect.top = 100
        self.rect.left = 120

    def move(self, Xmove, Ymove):
        self.rect.move_ip(Xmove, Ymove)

    def update(self, updateImage):
        self.updateImage.blit(self.imagePlayer, self.rect)



class Broom(pygame.sprite.Sprite):
    def __init__(self, enemies):
        self.enemiesList = []
        self.imageBroom = pygame.image.load('I+S/broomAnimated.jpg2.jpg')
        self.enemiesList.append(self.imageBroom)

        self.leftBroom = random.randrange(300, 600)
        self.topBroom = random.randrange(-400, -200)
        self.widthBroom = 13
        self.heightBroom = 32
        
        def enemies(self):
            for x in range(len(self.enemiesList)):
                if self.enemiesList[x].top > 2:
                    self.enemiesList[x]=(pygame.Rect(self.leftBroom, self.topBroom, self.widthBroom, self.heightBroom))

            

class Game(pygame.sprite.Sprite):
    
    def __init__(self): 
        width_window = 1040
        height_window = 704

        pygame.mixer.init()
        pygame.mixer.music.load('I+S/gameLoops.mp3')   #  background music
        pygame.mixer.music.play(-1)
        
        self.executusMeow = pygame.mixer.Sound('I+S/Cat_Meow.wav')    #  cat sound
    
        # GAME SCREEN  
        self.screen = pygame.display.set_mode((width_window, height_window))   
        self.background = pygame.image.load('I+S/indoor.png')
        pygame.display.set_caption("Executus time !")
        self.clock = pygame.time.Clock()


        self.executusImage = pygame.image.load('I+S/gus 2.png')
        self.player = Executus(self.executusImage)
        

    def start(self):
        self.game_over = False
        self.xMove = 0
        self.yMove = 0 
        self.speed = 8
        self.stop = 0
        self.collision = False


        while self.game_over == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    pygame.quit()
                    sys.exit()

            
                if self.collision == False:
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
            

            if self.collision(self.player, self.walls):


            self.screen.blit(self.background, (0, 0))
            




            pygame.display.flip()
            self.clock.tick(20)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.start()
    