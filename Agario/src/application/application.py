import pygame, math, random
from typing import List, Type, TypeVar

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

BLOB_COLOURS = [(80,252,54), (36,244,255), (243,31,46), (4,39,243), (254,6,178), (255,211,7), (216,6,254), (145,255,7), (7,255,182), (255,6,86), (147,7,255)]

class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Blob:
    blob_list = [] # how to add typing here
    def __init__(self, x: int, y: int):
        self.vec2 = Vector2(x, y)
        self.colour = BLOB_COLOURS[random.randrange(0, len(BLOB_COLOURS) - 1)]
        self.size = 9
        Blob.blob_list.append(self)

    @classmethod
    def draw(cls, window: pygame.Surface):
        for blob in Blob.blob_list:
            pygame.draw.circle(window, blob.colour, (blob.vec2.x, blob.vec2.y), blob.size)

    @classmethod
    def generate_blobs(cls, number_of_blobs: int):
        for i in range(number_of_blobs):
            blob = Blob(random.randrange(0, Application.WINDOW_WIDTH), random.randrange(0, Application.WINDOW_HEIGHT))
    
    @classmethod
    def check_blob_numbers(cls):
        if len(Blob.blob_list) < 25:
            cls.generate_blobs(7)

class Application:
    WINDOW_WIDTH: int = 0
    WINDOW_HEIGHT: int = 0
    blob_list: List[Blob] = []
    def __init__(self, name: str, WINDOW_WIDTH: int, WINDOW_HEIGHT: int, is_running: bool):
        Application.WINDOW_WIDTH = WINDOW_WIDTH
        Application.WINDOW_HEIGHT = WINDOW_HEIGHT

        self.name = name
        self.is_running = is_running
        self.player = Player('Player1', int(self.WINDOW_WIDTH/2), int(self.WINDOW_WIDTH/2))
        Blob.generate_blobs(30)
        Application.blob_list = Blob.blob_list
        self.camera = Camera(0, 0)
        self.map = Map()
        
    def start(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT)) #<class 'pygame.Surface'>
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
        self.camera.draw(self.window)

        pygame.display.flip()
        
    def shut_down(self):
        self.is_running = False

    def update(self):
        self.player.update()
        Blob.check_blob_numbers()
        self.camera.update(self.player)

    def draw_grid(self):
        line_colour = (230,240,240)
        for y in range(0, Application.WINDOW_HEIGHT, 25):
            pygame.draw.line(self.window, line_colour, (0, y), (Application.WINDOW_WIDTH, y), width = 3)
        
        for x in range(0, Application.WINDOW_WIDTH, 25):
            pygame.draw.line(self.window, line_colour, (x, 0), (x, Application.WINDOW_HEIGHT), width = 3)

class Player:
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.vec2 = Vector2(x, y)
        self.size = 20 #default size players start with is 15
        self.speed = 2
        self.score = 0

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

    def draw(self, window: pygame.Surface, font: pygame.font.Font):
        pygame.draw.circle(window, BLUE, (self.vec2.x, self.vec2.y), self.size)
        text = font.render(self.name, True, WHITE)
        text_rect = text.get_rect(center=(self.vec2.x, self.vec2.y))
        window.blit(text, text_rect)
        # Draw score
        self.draw_score(window, font)
        
    def check_collision_with_blob(self):
        for blob in Blob.blob_list:
            if (self.get_distance(self.vec2, blob.vec2)) < self.size + (blob.size/2):
                self.size += 0.5
                self.speed -= 0.001
                self.score += 1
                Blob.blob_list.remove(blob)
                print("[Speed]: {speed} [Size]: {size} [Score]: {score}".format(speed=self.speed, size=self.size, score = self.score)) 
           
    def get_distance(self, pos1: Vector2, pos2: Vector2) -> float:
        diff_x = math.fabs(pos1.x - pos2.x)
        diff_y = math.fabs(pos1.y - pos2.y)
        distance = math.sqrt(diff_x ** 2 + diff_y ** 2)
        return distance

    def draw_score(self, window: pygame.Surface, font: pygame.font.Font):
        transparent_rect = pygame.Surface((95,25), pygame.SRCALPHA) 
        transparent_rect.fill((50,50,50,80))
        message = f"Score: {self.score} "
        w, h = font.size(message)
        window.blit(pygame.transform.scale(transparent_rect, (w, h)), (8, Application.WINDOW_HEIGHT - 30))
        window.blit(font.render(message, True, (255,255,255)), (10, Application.WINDOW_HEIGHT - 30))

class Map:
    def __init__(self):
        self.scale = 3
        self.map_width = Application.WINDOW_WIDTH * self.scale
        self.map_height = Application.WINDOW_HEIGHT * self.scale

    def draw_grid(self, window: pygame.Surface):
        line_colour = (230,240,240)
        for y in range(0, self.map_height, 25):
            pygame.draw.line(window, line_colour, (0, y), (self.map_width, y), width = 3)
        
        for x in range(0, self.map_width, 25):
            pygame.draw.line(window, line_colour, (x, 0), (x, self.map_height), width = 3)

class Camera:
    def __init__(self, x: int, y: int):
        self.zoom = 0.45
        self.pos = Vector2(x, y)
        self.width = Application.WINDOW_WIDTH * self.zoom
        self.height = Application.WINDOW_HEIGHT * self.zoom
        self.view_point_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def update(self, player: Player): #limit player move within camera size
        self.pos = player.vec2
        self.view_point_rect = pygame.Rect(self.pos.x - self.width / 2, self.pos.y - self.height / 2, self.width, self.height)

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, RED, self.view_point_rect, width = 3)