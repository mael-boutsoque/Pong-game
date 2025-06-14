import pygame
from math import cos, sin, atan2, pi
from random import random

class Menu:
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.buttons = []
        self.load_buttons(game.switch_2_pong, game.switch_2_parameters,game.quit)
    
    def load(self):
        pass
    
    def load_buttons(self, start_game_function, launch_parameters_function, quit_game_function):
        self.buttons.append(Button((self.width-350)//2, (self.height-60)//2 + 60, 350, 60, "Start Game",50, start_game_function,text_color=(153, 153, 255)))
        self.buttons.append(Button((self.width-350)//2, (self.height-60)//2 + 60*3, 350, 60, "Settings",50, launch_parameters_function,text_color=(153, 153, 255)))
        self.buttons.append(Label(0, (self.height-300)//2 -100, self.width, 300, "PONG",256, text_color=(255,255,255),image1="",image2=""))
        self.buttons.append(ButtonIcon(self.width-100,self.height-100,50,50,quit_game_function,image1="images/buttons/quit1.png",image2="images/buttons/quit2.png"))
    
    def draw(self, display:pygame.Surface):
        for button in self.buttons:
            button.draw(display)
    
    def events(self, event:pygame.event.Event):
        for button in self.buttons:
            button.events(event)
    
    def run(self):
        pass
    

class Pong:
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.quit_function = game.switch_2_menu
        self.keys = game.keys
        self.load()
        self.load_images("images/buttons/bg.png")
    
    def load_images(self,path):
        self.bg = pygame.image.load(path)
    
    def load(self):
        player_width , player_height = 30,100
        self.player = Player(20,(self.width)//2-player_height,player_width,player_height,(0,self.height),keys=self.keys)
        self.enemy = Enemy(self.width-player_width-20,(self.width)//2-player_height,player_width,player_height,(0,self.height))
        
        self.ball = Ball(self.width//2,self.height//2,5,(0,self.width),(0,self.height))

    def draw(self, display:pygame.Surface):
        display.blit(self.bg,(0,min(0,self.ball.get_BouncesPlayer() + self.height - self.bg.get_height())))
        self.ball.draw(display)
        ball_pos = self.ball.get_pos()
        self.player.draw(display,ball_pos)
        self.enemy.draw(display,ball_pos)
    
    def events(self, event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit_function()
        
        self.player.events(event)
    
    def run(self):
        self.ball.run(self.player,self.enemy)


class Parameters:
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.buttons = []
        self.game_change_key = game.setkeys
        self.game_get_key = game.getkeys
        self.quit_function = game.switch_2_menu
        self.wait_key_for = None
        self.load_buttons(game.switch_2_menu)
    
    def load(self):
        pass
    
    def load_buttons(self, return_home_function):
        self.buttons.append(Label(0, 0, self.width, 130, "parameters",128, text_color=(255,255,255),image1="",image2=""))
        self.buttons.append(Button((self.width-350)//2, (self.height-60)//2 + 60, 350, 60, "Up",50, self.want_change_keyUp ,text_color=(153, 153, 255)))
        self.buttons.append(Button((self.width-350)//2, (self.height-60)//2 + 60*3, 350, 60, "Down",50, self.want_change_keyDown,text_color=(153, 153, 255)))
        self.buttons.append(ButtonIcon(self.width-50,self.height-50,30,30,return_home_function))
        self.buttons_wait_key = Label(100, (self.height-200)//2, self.width-200, 200, "Select a key",100, text_color=(153,153,255))
    
    def want_change_keyUp(self):
        self.want_change_key("up")
    def want_change_keyDown(self):
        self.want_change_key("down")
    def want_change_key(self,key:str):
        self.wait_key_for = key
    
    def change_key(self,key:str,result):
        keys = self.game_get_key()
        keys[key] = result
    
    def draw(self, display:pygame.Surface):
        if not self.wait_key_for:
            for button in self.buttons:
                button.draw(display)
        
        else:
            self.buttons_wait_key.draw(display)
    
    def events(self, event:pygame.event.Event):
        if not self.wait_key_for:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_function()
            for button in self.buttons:
                button.events(event)
        
        if not self.wait_key_for is None and event.type == pygame.KEYDOWN:
            if not event.key == pygame.K_ESCAPE:
                self.change_key(self.wait_key_for,event.key)
            
            self.wait_key_for = None
            print("keys :",self.game_get_key())
    
    def run(self):
        pass


class Player:
    def __init__(self,x,y,width,height,limity:tuple,keys:dict,images:str="images/buttons/plateforme all2.png"):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._dx,self._dy = 0,0
        self._limity = limity
        self._speed = 3
        self.keyUp = keys["up"]
        self.keyDown = keys["down"]
        self.lifes0 = 4
        self.lifes = self.lifes0
        self.load_images(images,5)
        self.load_hearts()
    
    def load_images(self,path,nb_states):
        self.sprites = []
        sprite_sheet = pygame.image.load(path).convert_alpha()
        sprite_width = 32
        sprite_height = 80
        for i in range(nb_states):
            rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
            image = sprite_sheet.subsurface(rect)
            image = pygame.transform.scale(image, (self._width, self._height))
            self.sprites.append(image)
    
    def load_hearts(self,path1="images/buttons/heart1.png",path0="images/buttons/heart0.png"):
        width,height = 23,20
        self.heart1 = pygame.image.load(path1)
        self.heart1 = pygame.transform.scale(self.heart1, (width,height))
        self.heart0 = pygame.image.load(path0)
        self.heart0 = pygame.transform.scale(self.heart0, (width,height))
    
    def draw(self,display:pygame.Surface,ball_pos:tuple):
        #pygame.draw.rect(display,(255,0,0),pygame.Rect(self._x,self._y,self._width,self._height))
        display.blit(self.sprites[self.lifes0-self.lifes],(self._x,self._y))
        self.run(ball_pos)
        y = display.get_height() - 30
        for i in range(self.lifes+1):
            display.blit(self.heart1,(10+30*i,y))
        for j in range(self.lifes+1,self.lifes0+1):
            display.blit(self.heart0,(10+30*j,y))
    
    def events(self,event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.keyDown:
                self._dy += self._speed
            if event.key == self.keyUp:
                self._dy -= self._speed
        
        elif event.type == pygame.KEYUP:
            if event.key == self.keyDown:
                self._dy -= self._speed
            if event.key == self.keyUp:
                self._dy += self._speed
    
    def get_rect(self)->pygame.Rect:
        return pygame.Rect(self._x,self._y,self._width,self._height)
    
    def run(self,ball_pos:tuple):
        self._y = min(max(self._y + self._dy,self._limity[0]),self._limity[1]-self._height)
    
    def damage(self,amount=1):
        if self.lifes == 0 and amount >0 :
            print("perdu")
        self.lifes = max(0,self.lifes-amount)
        print("damage",amount)

class Enemy(Player):
    def __init__(self, x, y, width, height, limity: tuple,images:str="images/buttons/plateforme enemy.png"):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._dx,self._dy = 0,0
        self._limity = limity
        self._speed = 3
        self.load_images(images,1)
        
    def event(self,event:pygame.event.Event):
        pass
    def run(self,ball_pos:tuple):
        go_up = self._y + 10 < ball_pos[1]
        go_down = self._y + self._height - 10 > ball_pos[1]
        if go_up or go_down:
            self._dy = self._speed * (go_up - go_down)
        self._y = min(max(self._y + self._dy,self._limity[0]),self._limity[1]-self._height)
    
    def draw(self,display:pygame.Surface,ball_pos:tuple):
        #pygame.draw.rect(display,(255,0,0),pygame.Rect(self._x,self._y,self._width,self._height))
        display.blit(self.sprites[0],(self._x,self._y))
        self.run(ball_pos)

class Ball:
    def __init__(self,x,y,radius,limitx:tuple,limity:tuple):
        self._x = x
        self._y = y
        self._radius = radius
        self._angle = 0
        self._limity = limity
        self._limitx = limitx
        self._speed = 3
        self.bouncePlayer = 0
    
    def move(self,player:Player,enemy:Enemy):
        oldx = self._x
        oldy = self._y
        self._x = min(max(self._x + self._speed * cos(self._angle),self._limitx[0]),self._limitx[1])
        self._y = min(max(self._y + self._speed * sin(self._angle),self._limity[0]),self._limity[1])
        
        if self._x < 1 and abs(self._angle)>pi/2:
            player.damage()
        
        players = [player.get_rect(),enemy.get_rect()]
        for player_rect in players:
            if player_rect.clipline(oldx,oldy,self._x,self._y):
                self._x,self._y = oldx,oldy
                
                if self._x > player_rect.right -1 or self._x < player_rect.left+1:
                    self._angle  -= pi + 2*self._angle + 0.2*random()
                    self.bouncePlayer += 1
                
                if self._y > player_rect.top -1 or self._y < player_rect.bottom+1:
                    self._angle = -self._angle
                    self.bouncePlayer += 1
                
        self._angle -= (pi + 2*self._angle + 0.2*random())*(self._x >= self._limitx[1] or self._x <= self._limitx[0])
        self._angle = (1-2*(self._y >= self._limity[1] or self._y <= self._limity[0]))*self._angle
    
    def run(self,player:Player,enemy:Enemy):
        self.move(player,enemy)
    
    def draw(self,display):
        pygame.draw.circle(display,(255,255,255),(self._x,self._y),self._radius)
    
    def get_pos(self) -> tuple[int,int]:
        return (self._x,self._y)
    
    def get_BouncesPlayer(self) -> int :
        return self.bouncePlayer
        

class Label:
    def __init__(self, x, y, width, height, text, text_size, image1 = "images/buttons/play1.png" , image2 = "images/buttons/play2.png" , text_color=(255,255,255), text_color_hover=(0,0,0) ):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self.hovered = False
        self._text_color = text_color
        self._text_color_hover = text_color_hover
        self.font = pygame.font.Font("ThaleahFat.ttf", text_size)
        self.image1 = self.load_image(image1)
        self.image2 = self.load_image(image2)
        self.update_draw()
    
    def move(self, x=None, y=None, width=None, height=None, text=None, text_size=None, text_color=None):
        self._x = x or self._x
        self._y = y or self._y
        self._width = width or self._width
        self._height = height or self._height
        self._text = text or self._text
        self._text_color = text_color or self._text_color
        if text_size:
            self.font = pygame.font.Font("ThaleahFat.ttf", text_size)
        if self.image1:
            self.image1 = pygame.transform.scale(self.image1, (self._width, self._height))
        if self.image2:
            self.image2 = pygame.transform.scale(self.image2, (self._width, self._height))
        self.update_draw()
    
    def load_image(self, image_path) -> pygame.Surface|None:
        try:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (self._width, self._height))
            return image
        except:
            return None

    def draw(self, display:pygame.Surface):
        display.blit(self.image, (self._x, self._y))
    
    def update_draw(self):
        if self.image1 and self.image2:
            self.image = self.image2.copy() if self.hovered else self.image1.copy()
        else:
            self.image = pygame.Surface((self._width, self._height), pygame.SRCALPHA)

        text_surface = self.font.render(self._text, False, self._text_color)
        rect = self.image.get_rect()
        text_rect = text_surface.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
        if self.hovered:
            hover_text_surface = self.font.render(self._text, False, self._text_color_hover)
            hover_text_rect = hover_text_surface.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2 + 5))
            self.image.blit(hover_text_surface,hover_text_rect)
        text_size = text_surface.get_size()

        if text_size[0] > self._width or text_size[1] > self._height:
            print(f"Warning: Text size exceeds button size, resizing button to ({text_size[0] + 20},{text_size[1] + 10})")
            self.move(self._x+(self._width-text_size[0] + 10),self._y+(self._height-text_size[1] + 20),text_size[0] + 20, text_size[1] + 10)
        
        else:
            self.image.blit(text_surface, text_rect)
        
    
    def events(self,event):
        pass


class Button(Label):
    def __init__(self, x, y, width, height, text, text_size, function, image1 = "images/buttons/play1.png" , image2 = "images/buttons/play2.png" , text_color=(255,255,255), text_color_hover=(0,0,0) ):
        super().__init__(x, y, width, height, text, text_size, image1, image2, text_color, text_color_hover)
        self.function = function
    
    
    def events(self,event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self._x, self._y, self._width, self._height).collidepoint(event.pos):
                if event.button == 1:
                    self.function()
        
        if event.type == pygame.MOUSEMOTION:
            if pygame.Rect(self._x, self._y, self._width, self._height).collidepoint(event.pos):
                self.hovered = True
                self.update_draw()
            elif self.hovered:
                self.hovered = False
                self.update_draw()

class ButtonIcon():
    def __init__(self, x, y, width, height, function, image1 = "images/buttons/home1.png" , image2 = "images/buttons/home2.png"):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.hovered = False
        self.function = function
        self.image1 = self.load_image(image1)
        self.image2 = self.load_image(image2)
        self.update_draw()
    
    def move(self, x=None, y=None, width=None, height=None):
        self._x = x or self._x
        self._y = y or self._y
        self._width = width or self._width
        self._height = height or self._height
        if self.image1:
            self.image1 = pygame.transform.scale(self.image1, (self._width, self._height))
        if self.image2:
            self.image2 = pygame.transform.scale(self.image2, (self._width, self._height))
        self.update_draw()
    
    def load_image(self, image_path) -> pygame.Surface|None:
        try:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (self._width, self._height))
            return image
        except:
            return None

    def draw(self, display:pygame.Surface):
        display.blit(self.image, (self._x, self._y))
    
    def update_draw(self):
        if self.image1 and self.image2:
            self.image = self.image2.copy() if self.hovered else self.image1.copy()
        else:
            self.image = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        
    
    def events(self,event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self._x, self._y, self._width, self._height).collidepoint(event.pos):
                if event.button == 1:
                    self.function()
        
        if event.type == pygame.MOUSEMOTION:
            if pygame.Rect(self._x, self._y, self._width, self._height).collidepoint(event.pos):
                self.hovered = True
                self.update_draw()
            elif self.hovered:
                self.hovered = False
                self.update_draw()
