import pygame

from dino_runner.components.dinossauro import Dinossauro
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.cloud_speed = 10 # velocidade da nuvem
        self.cloud_x1 = 200  # coordenada x da primeira nuvem
        self.cloud_y1 = 100  # coordenada y da primeira nuvem
        self.cloud_x2 = 600  # coordenada x da segunda nuvem
        self.cloud_y2 = 50   # coordenada y da segunda nuvem

        self.player = Dinossauro()
        self.obstacle_manager = ObstacleManager()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input) #chamando o metodo do player neste caso o dinossauro
        self.obstacle_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((0, 0, 0))
        self.draw_background()

        self.player.draw(self.screen) #chamar o metodo do player
        self.obstacle_manager.draw(self.screen) 
        
        #pygame.display.update()
        pygame.display.flip()


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(CLOUD, (self.cloud_x1, self.cloud_y1))  # desenho da primeira nuvem
        self.screen.blit(CLOUD, (self.cloud_x2, self.cloud_y2))  # desenho da segunda nuvem
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        if self.cloud_x1 < -64: #largura da nuvem
            self.cloud_x1 = SCREEN_WIDTH
        if self.cloud_x2 < -64: 
            self.cloud_x2 = SCREEN_WIDTH
        self.cloud_x1 -= self.cloud_speed # movendo a nuvem para a esquerda
        self.cloud_x2 -= self.cloud_speed 
        
