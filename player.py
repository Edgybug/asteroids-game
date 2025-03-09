import pygame
from circleshape import *
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        
        self.shoot_timer = 0
        self.score = 0 

        #survivability variables
        self.lifes = 3
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 3

        #movement variables
        self.rotation = 0
        self.acceleration = 0
        self.thrust_active = False
        self.reverse_active = False
        self.thrust_power = PLAYER_SPEED
        self.velocity = pygame.Vector2(0,0) #adding velocity vector 

        
    
    def draw(self, screen):
        # Make the player flash when invulnerable
        if self.invulnerable:
            # Flash effect - only draw during certain frames
            if pygame.time.get_ticks() % 200 < 100:  # Flash twice per second
                pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def update(self, dt):

        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.invulnerable_timer = 0

        self.shoot_timer -= dt

         # Store previous position to detect movement
        previous_position = self.position.copy()

        # Reset thrust active flag
        self.thrust_active = False
        self.reverse_active = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.thrust_active = True
            self.accelerate(dt)
        if keys[pygame.K_DOWN]:
            self.reverse_active = True
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Apply physics
        self.apply_physics(dt)

        # Check if player is moving
        self.is_moving = (previous_position != self.position)

    def apply_physics(self, dt):
         # Apply acceleration to velocity
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.thrust_active:
            # Only apply acceleration when thrusting
            self.velocity += forward * self.thrust_power *(1 + self.acceleration) * dt
        elif self.reverse_active:
        # Reverse thrust - notice the negative sign
            self.velocity -= forward * (self.thrust_power * 0.5) * dt  # Half speed for reverse
        else:
            # Auto-deceleration when not thrusting
            if self.velocity.length() > 0.1:
                self.velocity *= 0.98
        # Update position based on velocity
        self.position += self.velocity * dt

        # Keep player within screen boundaries
        # Left and right boundaries
        if self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x = 0  # Stop horizontal movement
        elif self.position.x > SCREEN_WIDTH - self.radius:
            self.position.x = SCREEN_WIDTH - self.radius
            self.velocity.x = 0  # Stop horizontal movement
        
        # Top and bottom boundaries
        if self.position.y < self.radius:
            self.position.y = self.radius
            self.velocity.y = 0  # Stop vertical movement
        elif self.position.y > SCREEN_HEIGHT - self.radius:
            self.position.y = SCREEN_HEIGHT - self.radius
            self.velocity.y = 0  # Stop vertical movement
       
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt 
    
    def move(self, dt):
        pass

    def accelerate(self, dt):
        if self.acceleration < MAX_ACCELERATION:
            self.acceleration += 0.005 * dt * 60
    
    def decelerate(self, dt):
        if self.acceleration > MIN_ACCELERATION:
            self.acceleration -= 0.005 * dt * 60
        else:
            self.acceleration = MIN_ACCELERATION

    def is_player_stationary(self):
        return self.velocity.length() < 0.1  # Adjust threshold as needed
        
    
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

        self.invulnerable = True
        player.invulnerable = self.invulnerable
        player.invulnerable_timer = player.invulnerable_duration

        return player
    

             
      
   
        
        


      

   
        