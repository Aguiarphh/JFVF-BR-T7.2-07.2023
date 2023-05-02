import pygame
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING

X_POS = 0
Y_POS = 310
Y_POS_DUCK = 340
JUMP_VEL = 8.5

class Dinossauro:
    def __init__(self):
        self.image = RUNNING[0]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS

        self.steps_count = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.jump_vel = JUMP_VEL

        self.x_vel = 0  # inicializa a velocidade do 0
        
    def update(self, user_input):
        if user_input[pygame.K_UP]:
            self.dino_jump = True
            self.dino_run = False
        elif user_input[pygame.K_DOWN]:
            self.dino_duck = True
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_run = True
        
        if user_input[pygame.K_LEFT]:
            self.x_vel = -5  # mover para a direita
        elif user_input[pygame.K_RIGHT]:
            self.x_vel = 5  # mover para a esquerda
        else:
            self.x_vel = 0  # para de se mover
        
        self.dino_rect.x += self.x_vel  # atualiza a posição X com base na velocidade
        
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()
        
        if self.steps_count > 9:
            self.steps_count = 0
    
    def run(self):
        self.image = RUNNING[self.steps_count//5]
        self.dino_rect.y = Y_POS
        self.steps_count += 1
    
    def duck(self):
        self.image = DUCKING[self.steps_count//5]
        self.dino_rect.y = Y_POS_DUCK
        self.steps_count += 1
    
    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel*4
            self.jump_vel -= 0.8
            if self.jump_vel < -JUMP_VEL:
                self.dino_rect.y = Y_POS
                self.dino_jump = False
                self.jump_vel = JUMP_VEL
    
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))