from pygame.locals import *
from random import randint
import pygame
import time
 
sprite_size = 22

class Apple:
    x = 0
    y = 0
    global sprite_size
    step = sprite_size
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 


class Wall:
    global sprite_size
    
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.step = sprite_size


    def draw(self, surface, image):
        for i in range(0, self.h, self.step):
            surface.blit(image,(0, i))
            surface.blit(image,(self.w - self.step, i))

        for i in range(0, self.w, self.step):
            surface.blit(image,(i, 0))
            surface.blit(image,(i, self.h - self.step))


 
class Player:
    x = [22]
    y = [22]
    global sprite_size
    step = sprite_size
    direction = 0
    length = 3
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       self.x[1] = 1*sprite_size
       self.x[2] = 2*sprite_size
 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
 
 
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False
 
class App:
    windowWidth = 800
    windowHeight = 600
    player = 0
    apple = 0
    global sprite_size
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.apple = Apple(5,5)

        self.wall = Wall(self.windowHeight, self.windowWidth)

        self.sprite_size = sprite_size
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)

        self._running = True
        self._image_surf = pygame.Surface([self.sprite_size - 4, self.sprite_size - 4])
        self._image_surf.fill((0, 255, 0))

        self._apple_surf = pygame.Surface([self.sprite_size - 4, self.sprite_size - 4])
        self._apple_surf.fill((255, 0, 0))

        self._wall_surf = pygame.Surface([self.sprite_size - 4, self.sprite_size - 4])
        self._wall_surf.fill((255, 0, 255))
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()
 
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i], 20):
                self.apple.x = randint(2,9) * sprite_size
                self.apple.y = randint(2,9) * sprite_size
                self.player.length = self.player.length + 1
 
 
        # does snake collide with itself?
        for i in range(2, self.player.length):
            if self.game.isCollision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], 20):
                print("Collision")
                exit(0)

        if self.player.x[0] < self.sprite_size or self.player.y[0] < self.sprite_size:
            print("collision")
            exit(1)

        if self.player.x[0] > self.windowWidth - self.sprite_size or self.player.y[0] > self.windowHeight - self.sprite_size:
            print("{}: {}:  Collision".format(self.player.x[0], self.player.y[0]))
            exit(1)
 
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.wall.draw(self._display_surf, self._wall_surf)

        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (50.0 / 1000.0);
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()