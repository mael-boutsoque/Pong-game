import pygame
pygame.init()
from utilities import *

class Game:
    def __init__(self,width, height):
        global sprites
        self.running = True
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pong Game")
        
        self.keys = {"up":pygame.K_UP,"down":pygame.K_DOWN}
        self.parameters = Parameters(width, height, self)
        self.menu = Menu(width, height, self)
        self.pong = Pong(width, height, self)
        self.death_screen = DeathScreen(width,height,self)
        
        self.active = self.menu

    
    def run(self):
        while self.running:
            self.update()
            self.active.run()
            self.draw()
            self.clock.tick(120)
        pygame.quit()
        print("game end")
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 1073741922:
                    print(self.pong.player.effects)
            if event.type == pygame.QUIT:
                pass
                #self.running = False
            else :
                self.active.events(event)
    
    def draw(self):
        self.display.fill((153, 153, 255))
        self.active.draw(self.display)
        pygame.display.flip()
    
    def switch_2_menu(self):
        self.active = self.menu
        self.active.load()
    def switch_2_pong(self):
        self.active = self.pong
        self.active.load()
    def switch_2_parameters(self):
        self.active = self.parameters
        self.active.load()
    def switch_2_death_screen(self):
        self.active = self.death_screen
        self.active.load()
    
    def setkeys(self,keys:dict):
        self.keys = keys
        self.pong.change_keys(self.keys)
    
    def getkeys(self):
        return self.keys
    
    def quit(self):
        self.running = False
