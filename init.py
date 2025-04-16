import pygame
import pymunk.pygame_util

#Pygame initialization
clock = pygame.time.Clock()
fps = 60

#Pymunk intitialization
space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = 0,1000      # Set its gravity

screen_blur = pygame.Surface((1024, 768), flags=pygame.SRCALPHA)
screen_blur.fill("white")
screen_blur.set_alpha(100)
screen_blur.set_colorkey("white")