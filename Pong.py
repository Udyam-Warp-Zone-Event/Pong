import os
import pygame
import sys
import time
import math
import random
from pygame.locals import *

pygame.init()

FPS = 40
scr_size = (width,height) = (600,400)

clock = pygame.time.Clock()

screen = pygame.display.set_mode(scr_size)
pygame.display.set_caption('Pong')

def displaytext(text,fontsize,x,y,color):
    font = pygame.font.SysFont('sawasdee', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)

def cpumove(cpu,ball):
    if ball.movement[0] > 0:
        if ball.rect.bottom > cpu.rect.bottom:
            cpu.movement[1] = 8
        elif ball.rect.top < cpu.rect.top:
            cpu.movement[1] = -8
        else:
            cpu.movement[1] = 0
    else:
        cpu.movement[1] = 0

class Paddle(pygame.sprite.Sprite):
    def __init__(self,x,y,sizex,sizey,color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.image = pygame.Surface((sizex,sizey),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        pygame.draw.rect(self.image,self.color,(0,0,sizex,sizey))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.points = 0
        self.movement = [0,0]

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def update(self):
        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        pygame.draw.rect(self.image,self.color,(0,0,self.sizex,self.sizey))
        screen.blit(self.image,self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,size,color,movement=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.movement = movement
        self.image = pygame.Surface((size,size),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,self.color,(self.rect.width/2,self.rect.height/2),size/2)
        self.rect.centerx = x
        self.rect.centery = y
        self.maxspeed = 10
        self.score = 0
        self.movement = movement

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def update(self):
        if self.rect.top == 0 or self.rect.bottom == height:
            self.movement[1] = -1*self.movement[1]
        if self.rect.left == 0:
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.movement = [random.randrange(-1,2,2)*4,random.randrange(-1,2,2)*4]
            self.score = 1
            #self.movement[0] = -1*self.movement[0]
        if self.rect.right == width:
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.movement = [random.randrange(-1,2,2)*4,random.randrange(-1,2,2)*4]
            self.score = -1

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        pygame.draw.circle(self.image,self.color,(self.rect.width/2,self.rect.height/2),self.size/2)
        screen.blit(self.image,self.rect)



def main():
    gameOver = False
    paddle = Paddle(width/10,height/2,width/60,height/8,(255,255,255))
    cpu = Paddle(width - width/10,height/2,width/60,height/8,(255,255,255))
    ball = Ball(width/2,height/2,12,(255,0,0),[4,4])
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddle.movement[1] = -8
                elif event.key == pygame.K_DOWN:
                    paddle.movement[1] = 8
            if event.type == pygame.KEYUP:
                paddle.movement[1] = 0

        cpumove(cpu,ball)

        screen.fill((0,0,0))
        paddle.draw()
        cpu.draw()
        ball.draw()

        displaytext(str(paddle.points),20,width/8,25,(255,255,255))
        displaytext(str(cpu.points),20,width - width/8,25,(255,255,255))

        if pygame.sprite.collide_mask(paddle,ball):
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1] - int(0.1*random.randrange(5,10)*paddle.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1*ball.maxspeed:
                ball.movement[1] = -1*ball.maxspeed

        if pygame.sprite.collide_mask(cpu,ball):
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1] - int(0.1*random.randrange(5,10)*cpu.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1*ball.maxspeed:
                ball.movement[1] = -1*ball.maxspeed

        if ball.score == 1:
            cpu.points += 1
            ball.score = 0
        elif ball.score == -1:
            paddle.points += 1
            ball.score = 0

        paddle.update()
        ball.update()
        cpu.update()

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()

main()
