import pygame

class Application:
    def __init__(self, name: 'str', SCREEN_WIDTH: 'int', SCREEN_HEIGHT: 'int', is_running: 'bool'):
        self.name = name
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.is_running = is_running

    def start(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Agar.io')
        self.is_running = True
        
    def shut_down(self):
        self.is_running = False

    def draw(self):
        print("drawing")
        self.window.fill((242, 251, 255)) #beige
        pygame.display.flip()

    def update(self):
        pass
