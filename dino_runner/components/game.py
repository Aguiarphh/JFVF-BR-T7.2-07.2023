import pygame

from dino_runner.components.dinossauro import Dinossauro
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD, HEART

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.playing = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.cloud_speed = 10 # velocidade da nuvem
        self.cloud_x1 = 200  # coordenada x da primeira nuvem
        self.cloud_y1 = 100  # coordenada y da primeira nuvem
        self.cloud_x2 = 600  # coordenada x da segunda nuvem
        self.cloud_y2 = 50   # coordenada y da segunda nuvem
        
        self.game_over = False
        
        self.paused = False

        self.lives = 3

        self.player = Dinossauro()
        self.obstacle_manager = ObstacleManager()

        self.score = 0
        self.death_count = 0

    def execute(self):
        self.executing = True
        
        while self.executing:
            if not self.playing:
                self.show_menu()
        
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.reset_game()
        
        while self.playing: 
            self.events()
            if self.paused:
                self.clock.tick(FPS)
                continue
            self.update()
            self.draw()

    def reset_game(self):
        self.score = 0
        self.game_speed = 10
        self.obstacle_manager.reset_obstacles()
        if self.lives == 0:
            self.game_over = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_c:
                    self.paused = False
            

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input) #chamando o metodo do player neste caso o dinossauro
        self.obstacle_manager.update(self)

        self.update_score()
        
    def update_score(self):
        self.score +=1
        
        if self.score % 100 == 0:
            self.game_speed+=5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((0, 0, 0))
        self.draw_background()

        self.player.draw(self.screen) #chamar o metodo do player
        self.obstacle_manager.draw(self.screen) 

        self.draw_score()
        #pygame.display.update()
        pygame.display.flip()

    def draw_score(self):
        FONT_STYLE = "freesansbold.ttf"
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score: {self.score}", True, (250,0,0))
        text2 = font.render(f"Lives: {self.lives}", True, (250,0,0))
        
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        
        self.screen.blit(text, text_rect)
        self.screen.blit(text2, (970, 100))

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
        
    def show_menu(self):
        self.screen.fill((255,255,255))
        
        half_screen_height = SCREEN_HEIGHT //2
        half_screem_width = SCREEN_WIDTH //2
                
        FONT_STYLE = "freesansbold.ttf"
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render("Press any key to start", True, (0,0,0))
        
        text_rect = text.get_rect()
        text_rect.center = (half_screem_width, half_screen_height)
        self.screen.blit(text, text_rect)
        
        text = font.render(f"Death: {self.death_count}", True, (255,0,0))
        text_rect.center = (150, 50)
        self.screen.blit(text, text_rect)
                
        pygame.display.flip()
        
        self.handle_events_on_menu()
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing == False
                self.executing = False
            elif event.type == pygame.KEYDOWN and self.game_over == False:
                self.run()