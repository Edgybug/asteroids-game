import pygame 
import sys
import os

from player import Player
from asteroid import Asteroid
from shot import Shot 
from explosions import Explosion

from asteroidfield import *
from constants import *

def main():
    
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Asteroids Game")
    clock = pygame.time.Clock()
    
   
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
   
    Asteroid.containers = (asteroids, drawable, updatable)
    Shot.containers = (shots, drawable, updatable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Explosion.containers = (updatable, drawable, explosion_group)

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
                    explosion = asteroid.explode()
                    explosion_group.add(explosion)

                    asteroid.split()

                    asteroid.kill()
                    shot.kill() 

                    player.player_score()
                    
        for asteroid in asteroids:
            if player.lifes > 0 and asteroid.collides_with(player):
                    print("Lost a life")
                    player = player.respawn()
            elif player.lifes <= 0 and asteroid.collides_with(player):
                    print("Game Over!")
                    sys.exit()
           
        screen.fill(BG_COLOR) 
 
        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        lives_text = font.render(f'Lives: {player.lifes}', True, (255, 255, 255))
        screen.blit(lives_text, (200, 10))

        acceleration_text = font.render(f'Acceleration level: {round(player.acceleration)}', True, (255, 255, 255))
        screen.blit(acceleration_text, (400, 10))

        pygame.display.flip()
 
        #limit the framerate to 60fps 
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()