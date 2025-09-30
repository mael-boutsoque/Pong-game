import pygame
pygame.init()
from utilities import *

#logs
from logger_config import setup_logger
log = setup_logger("client")

class Game:
    def __init__(self,width, height):
        global sprites
        self.running = True
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
        pygame.display.set_caption("Pong Game")
        
        self.keys = {"up":pygame.K_UP,"down":pygame.K_DOWN}
        self.parameters = Parameters(width, height, self)
        self.menu = Menu(width, height, self)
        self.pong = Pong(width, height, self)
        self.multiplayer = Multiplayer(width,height,self)
        self.death_screen = DeathScreen(width,height,self)
        self.host = Host(width,height,self)
        self.join = Join(width,height,self)
        self.select_ip = SelectIp(width,height,self.switch_2_join,self.switch_2_menu)
        
        self.active = self.menu

    
    def run(self):
        log.info("game started")
        while self.running:
            self.update()
            self.active.run()
            self.draw()
            self.clock.tick(120)
        pygame.quit()
        log.info("game end")
    
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
    
    def switch2mult(self,new_panel,connection:'Server|Client'):
        self.active = new_panel(self.width, self.height, self,connection)
        self.active.load()
    
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
    def switch_2_multiplayer(self):
        self.active = self.multiplayer
        self.active.load()
    def switch_2_host(self):
        self.active = self.host
        self.active.load()
    def switch_2_join(self,ip:str):
        self.active = self.join
        self.active.load(ip)
    def switch_2_selectip(self):
        self.active = self.select_ip
        self.active.load()
    
    def setkeys(self,keys:dict):
        self.keys = keys
        self.pong.change_keys(self.keys)
    
    def getkeys(self):
        return self.keys
    
    def quit(self):
        self.running = False


if __name__ == "__main__":
    game = Game(820,620)
    #game = Game(1920,1080)
    game.run()