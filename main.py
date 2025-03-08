import pygame 
from constants import *
from circleshape import *
from player import *

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Asteroids Game")
    running = True

    dt = 0 
    clock = pygame.time.Clock()
     
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        screen.fill(BG_COLOR)
        player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2) #define player to be in the middle of the screen
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        
    dt = clock.tick(60) / 1000 
    print(dt)

    

if __name__ == "__main__":
    main()