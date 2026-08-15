import pygame
from util.load_image import import_image
from entities.game_state import GameState

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

def menu(screen):
    print("Menu")

    width = screen.get_width()
    height = screen.get_height()

    clock = pygame.time.Clock()

    running = True
    mousedown = False
    mouseup = False

    start_img = import_image(f"resources/sprites/menu_buttons/start_game_button.png")
    start_down_img = import_image(f"resources/sprites/menu_buttons/start_game_button_down.png")
    load_img = import_image(f"resources/sprites/menu_buttons/load_game_button.png")
    load_down_img = import_image(f"resources/sprites/menu_buttons/load_game_button_down.png")
    exit_img = import_image(f"resources/sprites/menu_buttons/exit_button.png")
    exit_down_img = import_image(f"resources/sprites/menu_buttons/exit_button_down.png")

    while running:
        screen.fill((102, 204, 0))
        
        mouse = pygame.mouse.get_pos()
        start_pressed = False
        load_pressed = False
        exit_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
                mouseup = True

        if mousedown:
            if width/2-160 <= mouse[0] <=width/2+160 and 100 <= mouse[1] <= 180:
                start_pressed = True
                screen.blit(start_down_img, (width/2-160, 100))
            if width/2-160 <= mouse[0] <=width/2+160 and 200 <= mouse[1] <= 280:
                load_pressed = True
                screen.blit(load_down_img, (width/2-160, 200))
            if width/2-160 <= mouse[0] <=width/2+160 and 300 <= mouse[1] <= 380:
                exit_pressed = True
                screen.blit(exit_down_img, (width/2-160, 300))

        if mouseup:
            # Start Game
            if width/2-160 <= mouse[0] <=width/2+160 and 100 <= mouse[1] <= 180:
                print("Starting Game")
                game_state = GameState("uk")
                return "location", game_state
            # Load Game
            if width/2-160 <= mouse[0] <=width/2+160 and 200 <= mouse[1] <= 280:
                print("Loading Game")
            # Exit
            if width/2-160 <= mouse[0] <=width/2+160 and 300 <= mouse[1] <= 380:
                print("Exiting Game")
                running = False

        if not (mousedown and start_pressed):
            screen.blit(start_img, (width/2-160, 100))
        if not (mousedown and load_pressed):
            screen.blit(load_img, (width/2-160, 200))
        if not (mousedown and exit_pressed):
            screen.blit(exit_img, (width/2-160, 300))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()