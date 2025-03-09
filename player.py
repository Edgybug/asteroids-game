import pygame
from circleshape import *
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.score = 0 
        self.lifes = 3
        self.acceleration = 0
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.move(dt)
            self.accelerate()
        if keys[pygame.K_DOWN]:
            self.move(-dt)
            self.decelerate()
        if keys[pygame.K_SPACE]:
            self.shoot()
       
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt 
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * self.acceleration

    
    def accelerate(self):
        if self.acceleration > MAX_ACCELERATION:
            return
        self.acceleration += 0.005
    
    def decelerate(self):
        if self.acceleration <= MIN_ACCELERATION:
            return
        self.acceleration -= 0.005
    

    def shoot(self):    
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED 
    
    def player_score(self):
        self.score += SCORE_INCREMENT
          
    def respawn(self):
        self.kill()
        if self.lifes <= 0:
            return 
        self.lifes -= 1
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        player.lifes = self.lifes
        player.score = self.score
        return player
        
             
      
   
        
        


      

   
        