import pygame
from util.load_image import import_image
from util.font import write_string

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

def end_screen(screen, game_state):
    print("Menu")

    width = screen.get_width()
    height = screen.get_height()

    clock = pygame.time.Clock()

    running = True
    mousedown = False
    mouseup = False

    finish_img = import_image(f"resources/sprites/button_finish.png")

    score = game_state.get_score()
    

    while running:
        screen.fill((102, 204, 0))
        
        mouse = pygame.mouse.get_pos()
        start_pressed = False
        load_pressed = False
        exit_pressed = False

        write_string(screen, f"Congratulations! You made it to {game_state.end_point}!", 100, 100)
        write_string(screen, f"You scored {score} points!", 100, 140)

        if 100 <= mouse[0] <= 220 and 200 <= mouse[1] <= 256:
            screen.blit(finish_img, (100, 204))
            write_string(screen, "Finish", 112, 220)
        else:
            screen.blit(finish_img, (100, 200))
            write_string(screen, "Finish", 112, 216)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
                mouseup = True
                if 100 <= mouse[0] <= 220 and 200 <= mouse[1] <= 256:
                    return "menu", game_state


        pygame.display.flip()
        clock.tick(30)

    pygame.quit()