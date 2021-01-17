import sys
import pygame
from pygame.locals import *
import random

pygame.init()
screen=pygame.display.set_mode((600,600))
clock=pygame.time.Clock()

BCK=pygame.image.load('snake_gallery/welcome.png').convert()
OVER=pygame.image.load('snake_gallery/over.png').convert()

COL=[(225,250,200),(0,0,0)]

SCREEN_WIDTH=600
SCREEN_HEIGHT=600

GRID_WIDTH=SCREEN_WIDTH/30
GRID_HEIGHT=SCREEN_HEIGHT/30
GRID_SIZE=30

up=(0,-1)
down=(0,1)
left=(-1,0)
right=(1,0)

class Snake(object):
    def __init__(self):
        self.color=(255,65,45)
        self.width=30
        self.position=[((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))]
        self.direction=random.choice([up,down,left,right])
        self.length=1
        self.score=0
        self.speed=7

    def head_pos(self):
        return self.position[0]

    def draw(self,surface):
        for p in self.position:
            r=pygame.Rect((p[0],p[1]),(self.width,self.width))
            pygame.draw.rect(surface,self.color,r)

    def reset(self):
        self.color=(255,65,45)
        self.width=30
        self.position=[((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))]
        self.direction=random.choice([up,down,left,right])
        self.length=1

    
    def move(self):
        pos=self.head_pos()
        x,y=self.direction
        new_pos=(((pos[0]+(x*self.width))%SCREEN_WIDTH),(pos[1]+(y*self.width))%SCREEN_HEIGHT)
        if len(self.position) > 2 and new_pos in self.position[2:]:
            game_over()
        else:
            self.position.insert(0,new_pos)
            if len(self.position)>self.length:
                self.position.pop()

    def turn(self,coordinate):
        if self.length > 1 and (coordinate[0]*-1, coordinate[1]*-1) == self.direction:
            return
        else:
            self.direction=coordinate

    def take_events(self):
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_UP or event.key==K_w:
                    self.turn(up)
                elif event.key==K_DOWN or event.key==K_s:
                    self.turn(down)
                elif event.key==K_LEFT or event.key==K_a:
                    self.turn(left)
                elif event.key==K_RIGHT or event.key==K_d:
                    self.turn(right)
        
def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            r2=pygame.Rect(((x*GRID_SIZE),(y*GRID_SIZE)),(GRID_SIZE,GRID_SIZE))
            pygame.draw.rect(surface,(255,255,255),r2)

class Food(object):
    def __init__(self):
        self.position=(0,0)
        self.color=(65,84,62)

    def rand_pos(self):
        self.position=(random.randint(0,(GRID_WIDTH-1))*GRID_SIZE,random.randint(0,(GRID_HEIGHT-1))*GRID_SIZE)
    
    def draw(self,surface):
        r=pygame.Rect((self.position[0],self.position[1]),(GRID_SIZE,GRID_SIZE))
        pygame.draw.rect(surface,self.color,r)

def welcome_screen():
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and event.key==K_p:
                game()
            else:
                screen.blit(BCK,(0,0))
                pygame.display.update()

text_font = pygame.font.SysFont("monospace",16)

def game():
    food=Food()
    snake=Snake()
    drawGrid(screen)
    food.rand_pos()
    while True:
        snake.take_events()
        drawGrid(screen)
        snake.move()
        snake.draw(screen)
        if snake.head_pos()==food.position:
            snake.length+=1
            snake.score+=1
            food.rand_pos()
        if snake.score>0 and snake.score%5==0:
            food.color=(255,150,241)
        elif snake.score%5!=0:
            food.color=(65,84,62)
        food.draw(screen)
        score=text_font.render("YOUR SCORE {0}".format(snake.score),1,(0,0,0))
        screen.blit(score,(8,15))
        clock.tick(snake.speed)
        pygame.display.update()

def game_over():
    screen.blit(OVER,(0,0))
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and event.key==K_r:
                game()
            else:
                clock.tick(30)
                screen.blit(OVER,(0,0))
        pygame.display.update()

welcome_screen()