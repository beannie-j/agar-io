import pygame, math, random

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

BLOB_COLOURS = [(80,252,54), (36,244,255), (243,31,46), (4,39,243), (254,6,178), (255,211,7), (216,6,254), (145,255,7), (7,255,182), (255,6,86), (147,7,255)]

class Application:
    SCREEN_WIDTH, SCREEN_HEIGHT = 0, 0
    blob_list = []
    def __init__(self, name: 'str', SCREEN_WIDTH: 'int', SCREEN_HEIGHT: 'int', is_running: 'bool'):
        self.name = name
        Application.SCREEN_WIDTH = SCREEN_WIDTH
        Application.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.is_running = is_running
        self.player = Player('Player1', self.SCREEN_WIDTH/2, self.SCREEN_WIDTH/2)
        Blob.generate_blobs(20)
        Application.blob_list = Blob.blob_list
        print(len(Application.blob_list))
        
    def start(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT)) #<class 'pygame.Surface'>
        pygame.font.init()
        try:
            self.font = pygame.font.Font('../../Assets/OpenSans-Regular.ttf', 11)
        except:
            print("Font file not found")
            self.font = pygame.font.SysFont("comicsans", 14)
        pygame.display.set_caption('Agar.io')
        self.is_running = True

    def draw(self):
        self.window.fill((242, 251, 255)) #beige
        self.draw_grid()
        self.player.draw(self.window, self.font)
        Blob.draw(self.window)
        pygame.display.flip()
        
    def shut_down(self):
        self.is_running = False

    def update(self):
        self.player.update()
        Blob.check_blob_numbers()

    def draw_grid(self):
        pass

class Vector2:
    def __init__(self, x: 'int', y: 'int'):
        self.x = x
        self.y = y

class Blob:
    blob_list = []
    def __init__(self, x: 'int', y: 'int'):
        self.vec2 = Vector2(x, y)
        self.colour = BLOB_COLOURS[random.randrange(0, len(BLOB_COLOURS) - 1)]
        self.size = 9
        Blob.blob_list.append(self)

    @classmethod
    def draw(cls, window: 'pygame.Surface'):
        for blob in Blob.blob_list:
            pygame.draw.circle(window, blob.colour, (blob.vec2.x, blob.vec2.y), blob.size)

    @classmethod
    def generate_blobs(cls, number_of_blobs: 'int'):
        for i in range(number_of_blobs):
            blob = Blob(random.randrange(0, Application.SCREEN_WIDTH), random.randrange(0, Application.SCREEN_HEIGHT))
    
    @classmethod
    def check_blob_numbers(cls):
        if len(Blob.blob_list) < 15:
            cls.generate_blobs(5)


class Player:
    def __init__(self, name: 'str', x: 'int', y: 'int'):
        self.name = name
        self.vec2 = Vector2(x, y)
        self.size = 20 #default size players start with is 15
        self.speed = 0.1
        self.points = 0

    def update(self):
        self.move()
        self.check_collision_with_blob()
        
    def move(self):
        mx, my = pygame.mouse.get_pos()
        toMouse = Vector2(mx, my)

        toMouse.x = mx - self.vec2.x
        toMouse.y = my - self.vec2.y

        distance_to_mouse = math.sqrt(toMouse.x * toMouse.x + toMouse.y * toMouse.y)

        toMouse.x = toMouse.x / distance_to_mouse
        toMouse.y = toMouse.y / distance_to_mouse

        toMouse.x = toMouse.x * self.speed
        toMouse.y = toMouse.y * self.speed

        self.vec2.x += toMouse.x
        self.vec2.y += toMouse.y

    def draw(self, window: 'pygame.Surface', font: 'pygame.font.Font'):
        pygame.draw.circle(window, BLUE, (self.vec2.x, self.vec2.y), self.size)
        text = font.render(self.name, True, WHITE)
        text_rect = text.get_rect(center=(self.vec2.x, self.vec2.y))
        window.blit(text, text_rect)

    def check_collision_with_blob(self):
        for blob in Blob.blob_list:
            if (self.get_distance(self.vec2, blob.vec2)) < self.size + (blob.size/2):
                self.size += 0.5
                Blob.blob_list.remove(blob)
            
    def get_distance(self, pos1: 'Vector2', pos2: 'Vector2') -> float:
        diff_x = math.fabs(pos1.x - pos2.x)
        diff_y = math.fabs(pos1.y - pos2.y)
        distance = math.sqrt(diff_x ** 2 + diff_y ** 2)
        return distance


