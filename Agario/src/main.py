import pygame
from application.application import Application

application = Application("Agar.io", 600, 600, False)

def main():
    application.start()

    while application.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                application.shut_down()
                
        application.draw()
    
    pygame.quit()

if __name__=="__main__":
    main()