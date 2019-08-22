import pygame , sys



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


    def start(self):
        self.game_over = False


        while self.game_over == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    pygame.quit()
                    sys.exit()


            self.screen.blit(self.background, (0, 0))
            
            pygame.display.flip()
            self.clock.tick(20)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.start()
    