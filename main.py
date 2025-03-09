import pygame 
import sys

from player import Player
from asteroid import Asteroid
from shot import Shot 

from asteroidfield import *
from constants import *

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Asteroids Game")
    clock = pygame.time.Clock()
   
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, drawable, updatable)
    Shot.containers = (shots, drawable, updatable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) #define player to be in the middle of the screen

    dt = 0 
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)     

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.kill()
                    asteroid.split()
                    shot.kill()
                    
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()
                 
        screen.fill(BG_COLOR) 
 
        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        #limit the framerate to 60fps
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()