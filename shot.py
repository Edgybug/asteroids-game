import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, SHOT_RADIUS)
        self.image = pygame.image.load("img/shot.png")  # Load the image
        self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image down

    def draw(self, screen):
        #pygame.draw.circle(screen, (255,255,255), self.position, self.radius, 2)
        screen.blit(self.image, (self.position.x, self.position.y))
    
    def update(self, dt):
        self.position += self.velocity * dt 