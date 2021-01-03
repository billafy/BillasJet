import pygame as pg
import random as rd

from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT) # imports the up down left right and other keys 

pg.init() # initializes the all the pygame functions

logo = pg.image.load("download.jpg") # loading the game icon

SCREEN_WIDTH = 800 # setting screen width
SCREEN_HEIGHT = 600 # setting screen height

class Player(pg.sprite.Sprite) : # Surface drawn for the player which we will control
    def __init__(self) : 
        super(Player,self).__init__()
        self.surf = pg.image.load("jet.png").convert() # surface of width 75 and height 25
        self.surf.set_colorkey((255,255,255),RLEACCEL) # colour of the surface
        self.rect = self.surf.get_rect() # shape of the surface
        
    def update(self,pressed_keys) : # this function updates the player movements
        if pressed_keys[K_UP]: # up
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN] : # down
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]: # left
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]: # right
            self.rect.move_ip(5,0)
            
        if self.rect.left < 0 : # these conditions are to stop the object going out of the screen
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH :
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= SCREEN_HEIGHT :
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top <= 0 :
            self.rect.top = 0
            
class Enemy(pg.sprite.Sprite) :# Surface drawn for the enemies 
    
    def __init__(self) : 
        super(Enemy,self).__init__()
        self.surf = pg.image.load("missile.png").convert() # enemy surface size
        self.surf.set_colorkey((255,255,255),RLEACCEL) # enemy surface color
        self.rect = self.surf.get_rect( # spawning of the enemy
            center = (
                rd.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                rd.randint(0,SCREEN_HEIGHT),
                )
            )
        self.speed = rd.randint(2,5) # enemy speed which will range from 5 to 20
        
    def update(self) : # movement of the enemy
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0 : # if enemy passes the left edge it vanishes
            self.kill()
 
class Cloud(pg.sprite.Sprite) : # Surface drawn for the clouds
    def __init__(self) : 
        super(Cloud,self).__init__()
        self.surf = pg.image.load("cloud.png").convert() # loading cloud image
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                rd.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100),
                rd.randint(0,SCREEN_HEIGHT)
                )
            )
    def update(self) : # cloud will vanish when it touches the left edge
        self.rect.move_ip(-1,0)
        if self.rect.right < 0 : 
            self.kill()
    

add_Enemy = pg.USEREVENT + 1 
pg.time.set_timer(add_Enemy,250) # timer to set 250 milliseconds, new enemy spawn rate 

add_Cloud = pg.USEREVENT + 2
pg.time.set_timer(add_Cloud,1000) # add a cloud every 500 milliseconds 
        
pg.display.set_icon(logo) # setting game icon
pg.display.set_caption("Game") # setting game name or caption
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # setting screen size

player = Player() # creating a Player object

clouds = pg.sprite.Group() # creates a group of clouds
enemies = pg.sprite.Group() # creates a group of enemies
all_sprites = pg.sprite.Group()
all_sprites.add(player) 

running = True # game is running?

while running : 
    for event in pg.event.get() : # gets the input from user
        if event.type==KEYDOWN : # checks what key
            if event.key == K_ESCAPE : # if user clicks escape, quit the loop
                running = False
        elif event.type == pg.QUIT  : # if users clicks quit button, quit the loop
            running = False
        elif event.type == add_Enemy : 
            new_Enemy = Enemy() # creating a new enemy object
            enemies.add(new_Enemy) # add it into the enemies sprite group
            all_sprites.add(new_Enemy) # add it into the all_sprites sprite group
        elif event.type == add_Cloud : 
            new_Cloud = Cloud() # creating a new cloud object
            clouds.add(new_Cloud) # adding it to the sprites group
            all_sprites.add(new_Cloud)
           
    pressed_keys = pg.key.get_pressed() # gets the set of key pressed by users
    
    clouds.update() # updates the cloud position
    player.update(pressed_keys) # calls the update function and passed the key pressed
    enemies.update() # will update the enemy position 
    
    screen.fill((135,206,250)) # fill the screen with blue color(sky)
    
    for entity in all_sprites : 
        screen.blit(entity.surf,entity.rect) # blitting all surfaces
        
    if pg.sprite.spritecollideany(player,enemies) : # if player and enemy collide, the game will stop
        player.kill()
        running = False
                    
    pg.display.flip()
    
pg.quit()

