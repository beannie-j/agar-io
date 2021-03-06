import pygame
from application.application import Application, Camera

application = Application("Agar.io", 800, 600, False)
clock = pygame.time.Clock()
FPS = 60

def main():
    application.start()
    pause = False
    while application.is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                application.shut_down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    application.shut_down()
                if event.key == pygame.K_p:
                    pause = True
                if event.key == pygame.K_r:
                    pause = False
        if pause == False:
            application.update()  
            application.draw()
    pygame.quit()

if __name__=="__main__":
    main()