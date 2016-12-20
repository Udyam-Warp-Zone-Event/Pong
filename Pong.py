"""
Pong
Written By : Shivam Shekhar
"""

#importing libraries
import os
import pygame
import sys
import time
import math
import random
from pygame.locals import *

#initializing pygame
pygame.init()

#setting the FPS or number of Frames per Second
FPS = 60

#Setting the screen size
scr_size = (width,height) = (600,400)

#creating a clock object from pygame.time.Clock class
clock = pygame.time.Clock()

#Declaring various color values
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

"""
Creating our game screen by passing its screen size as the parameter,
and setting its caption as 'Pong'
"""
screen = pygame.display.set_mode(scr_size)
pygame.display.set_caption('Pong')

"""
A function used to display text on the screen
It takes in 4 parameters, i.e
text : the text which is to be printed. Has to be a string
fontsize : the fontsize of the text to be printed. Must be an integer
x,y : The x and y coordinates where we want our text to be printed
color : The color of the text. Its has to be in (R,G,B) format where R, G and B takes values from 0 to 255
"""
def displaytext(text,fontsize,x,y,color):
    font = pygame.font.SysFont('sawasdee', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)

"""
A function which moves the CPU's paddle
The concept behind this function is the same as that used in the real world,i.e
the CPU paddle will try to chase the ball based on its coordinates
"""
def cpumove(cpu,ball):
    if ball.movement[0] > 0: #ensures that the CPU moves only when the ball is directed towards it
        #the extra addition of cpu.rect.height/5 ensures that the CPU will miss the ball sometimes
        if ball.rect.bottom > cpu.rect.bottom + cpu.rect.height/5:
            cpu.movement[1] = 8
        elif ball.rect.top < cpu.rect.top - cpu.rect.height/5:
            cpu.movement[1] = -8
        else:
            cpu.movement[1] = 0
    else:
        cpu.movement[1] = 0

"""
A paddle class which represents a real world Paddle.
The class is initialized by passing 5 parameters, i.e
x,y : the x and y coordinates of the paddle to determine its position
sizex,sizey : the width and height of the paddle which determines its size
color : the color of the paddle in (R,G,B) format
"""
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

    #A function which checks whether the paddle is going out of bounds and make corrections accordingly
    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    #An update function which updates the state and position of the paddle
    def update(self):
        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    #A draw function which draws our paddle onto the screen
    def draw(self):
        #pygame.draw.rect(self.image,self.color,(0,0,self.sizex,self.sizey))
        screen.blit(self.image,self.rect)

"""
Just like the Paddle class, this is a Ball class which represents a real world ball
It is also initialized by taking in 5 parameters, i.e
x,y : x and y coordinates of where the ball is to be placed initially
size : the diameter of the ball
color : color of the ball in (R,G,B) format
movement : determines how much the ball will move initially (in pixels) in [x,y] direction.
           It is [0,0] by default.
"""
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
        pygame.draw.circle(self.image,self.color,(int(self.rect.width/2),int(self.rect.height/2)),int(size/2))
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

    #This update functions detemines how the ball will move
    def update(self):
        if self.rect.top == 0 or self.rect.bottom == height: #reverses the vertical velocity on collision with top and bottom walls
            self.movement[1] = -1*self.movement[1]
        if self.rect.left == 0: #resets the ball's position and notes that the point is scored by the CPU
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.movement = [random.randrange(-1,2,2)*4,random.randrange(-1,2,2)*4]
            self.score = 1

        if self.rect.right == width: #resets the position of the ball and notes that the point is scored by the user
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.movement = [random.randrange(-1,2,2)*4,random.randrange(-1,2,2)*4]
            self.score = -1

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        pygame.draw.circle(self.image,self.color,(int(self.rect.width/2),int(self.rect.height/2)),int(self.size/2))
        screen.blit(self.image,self.rect)


#The main function of our program
def main():
    gameOver = False #Sets the initial state of the game
    paddle = Paddle(width/10,height/2,width/60,height/8,white) #creating an object for the user's paddle
    cpu = Paddle(width - width/10,height/2,width/60,height/8,white) #creating an object for the CPU's paddle
    ball = Ball(width/2,height/2,12,red,[4,4]) #creating an object for the ball

    while not gameOver: #running our game loop
        for event in pygame.event.get(): #checks for various events in pygame, like keypress, mouse movement, etc
            if event.type == pygame.QUIT: #checks, if the user has clicked the close button
                quit()                    #quits the program

            if event.type == pygame.KEYDOWN: #checks whether a key has been pressed or not
                if event.key == pygame.K_UP: #If user has pressed the UP key
                    paddle.movement[1] = -8  #Paddle moves upwards
                elif event.key == pygame.K_DOWN: #If user has pressed the down key
                    paddle.movement[1] = 8       #Paddle moves downwards
            if event.type == pygame.KEYUP:    #If the user lifts the key
                paddle.movement[1] = 0        #Paddle stops moving

        cpumove(cpu,ball) #moves the CPU's paddle

        screen.fill(black) #fills the entire screen with black color

        #drawing user's paddle, cpu's paddle and ball
        paddle.draw()
        cpu.draw()
        ball.draw()

        #displaying the points scored by the user and cpu
        displaytext(str(paddle.points),20,width/8,25,(255,255,255))
        displaytext(str(cpu.points),20,width - width/8,25,(255,255,255))

        """
        using pygame.sprite.collide_mask function to check for 'pixel perfect' collision
        between user's and cpu's paddle with the ball

        The collision is based on the real world concept of perfectly elastic collisions.
        hence, whenever the ball strikes the paddle (placed vertically), the horizontal velocity is reversed,
        while the vertical velocity is equal to the relative velocity of ball w.r.t the paddle.
        In order to add some randomness, some error is introduced to the relative velocity of the ball and the paddle, i.e
        The paddle's velocity is multiplied by a factor between 0.5 to 1 before calculating the relative velocity.

        """
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

        #checks whether user or cpu scored a point and increments accordingly
        if ball.score == 1:
            cpu.points += 1
            ball.score = 0
        elif ball.score == -1:
            paddle.points += 1
            ball.score = 0

        #updating the states of user's paddle, cpu's paddle and ball
        paddle.update()
        ball.update()
        cpu.update()

        #updating the entire display"""
        pygame.display.update()

        #adding the time delay based on the number of 'Frames per Second'
        clock.tick(FPS)

    #Exiting the program by safely quitting pygame
    pygame.quit()
    quit()

#calling our main function
main()
