import pygame
import random
from circleshape import *
from constants import *
from explosions import Explosion

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.image = pygame.image.load("img/asteroid.png")  # Load the image
        self.image = pygame.transform.scale(self.image, (radius, radius))  # Scale the image down
    
    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))
    
    def update(self, dt):
        self.position += self.velocity * dt 
    
    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20,50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a1.velocity = self.velocity.rotate(random_angle) * 1.2
        a2 = Asteroid(self.position.x, self.position.y, new_radius)
        a2.velocity = self.velocity.rotate(-random_angle) * 1.2
   
        