import pygame
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, SCREEN_WIDTH, DEFAULT_TYPE, SHIELD_TYPE, RUNNING_SHIELD, DUCKING_SHIELD,JUMPING_SHIELD, HAMMER_TYPE, RUNNING_HAMMER, DUCKING_HAMMER, JUMPING_HAMMER

RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}

X_POS = 0
Y_POS = 310
Y_POS_DUCK = 340
JUMP_VEL = 8.5
WALK = 10

class Dinossauro:
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[DEFAULT_TYPE][0]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS

        self.steps_count = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.jump_vel = JUMP_VEL

        self.has_power_up = False

        self.invisible = False
        self.invisible_ticke = 0
        
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
        
        if self.dino_rect.x < 0:
            self.dino_rect.x = 0   #  limitando o dino de acordo com a largura da tela
        elif self.dino_rect.x + self.dino_rect.width > SCREEN_WIDTH:
            self.dino_rect.x = SCREEN_WIDTH - self.dino_rect.width

        self.dino_rect.x += self.x_vel  # atualiza a posição X com base na velocidade
        
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()
        
        if self.steps_count > 9:
            self.steps_count = 0
        
        if self.invisible_ticke > 0:
            self.invisible_ticke -= 1
            self.invisible  = True
        else:
            self.invisible = False
    
    def run(self):
        #self.image = RUNNING[self.steps_count//5]
        self.image = RUN_IMG[self.type][self.steps_count//5]

        self.dino_rect.y = Y_POS
        self.steps_count += 1
    
    def duck(self):
        #self.image = DUCKING[self.steps_count//5]
        self.image = DUCK_IMG[self.type][self.steps_count//5]

        self.dino_rect.y = Y_POS_DUCK
        self.steps_count += 1
    
    def jump(self):
        #self.image = JUMPING
        self.image = JUMP_IMG[self.type]

        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel*4
            self.jump_vel -= 0.8

        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL
    
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
