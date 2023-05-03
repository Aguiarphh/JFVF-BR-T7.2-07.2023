import pygame
import random

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, SCREEN_WIDTH, BIRD
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

class ObstacleManager:
    
    def __init__(self):
        self.obstacles = []
        self.birds = []
        self.bird_frames = 0

    def update(self, game):
        if len(self.obstacles) == 0:
            small_cactus = Cactus(SMALL_CACTUS[random.randint(0, 2)])
            large_cactus = Cactus(LARGE_CACTUS[random.randint(0, 2)])
            

            # Define as posições iniciais dos cactos
            large_cactus.rect.x = SCREEN_WIDTH + small_cactus.rect.width + 300
            large_cactus.rect.y = 310

            # Adiciona os cactos à lista de obstáculos
            self.obstacles.append(small_cactus)
            self.obstacles.append(large_cactus)
            
            bird = None
            if random.randint(0, 1) == 0:
                bird = Bird(BIRD[0])
            else:
                bird = Bird(BIRD[1])
            
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break

        self.bird_frames += 1
        if self.bird_frames == 200:
            bird = Bird(BIRD[random.randint(0, 1)])
            bird.rect.x = SCREEN_WIDTH + random.randrange(500) # Define a posição X do pássaro
            bird.rect.y = random.randrange(90) # Define a posição Y do pássaro
            self.birds.append(bird) # Adiciona o novo pássaro à lista de obstáculos
            self.bird_frames = 0

        # Atualiza e desenha os pássaros
        for bird in self.birds:
            bird.update(game.game_speed, self.obstacles)
            if bird.rect.x < -bird.rect.width:
                self.birds.remove(bird)
            bird.draw(game.screen)
            
            # Verifica a colisão entre o jogador e os pássaros
            if game.player.dino_rect.colliderect(bird.rect):
                pygame.time.delay(500)
                game.playing = False
                break   

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

        for bird in self.birds:
            bird.draw(screen) 
        