import pygame
from util.load_image import import_image
from util.font import write_string
from scenes.wallet import show_wallet
from scenes.flop import flop_overlay

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

def location_scene(screen, game_state):
    print("Home")
    
    pygame.init()

    width = screen.get_width()
    height = screen.get_height()
    mask_wallet = False
    mask_flop = game_state.need_flop

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, size=30)

    running = True
    current_loc = game_state.route[-1]
    map_img = import_image(f"resources/sprites/menu_buttons/map_button.png")
    wallet_img = import_image(f"resources/sprites/menu_buttons/wallet_button.png")
    departres_img = import_image(f"resources/sprites/menu_buttons/departures_button.png")
    background_img = import_image(f"resources/sprites/backgrounds/background3.png")
    mask_img = import_image(f"resources/sprites/backgrounds/mask.png")
    char_img = import_image(f"resources/sprites/char/char2.png")
    clock_img = import_image(f"resources/sprites/clock.png")
    close_img = import_image("resources/sprites/button_close.png")

    ticket_buttons = []

    while running:
        screen.blit(background_img, (0,0))
        
        write_string(screen, current_loc, 200, 440)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not (mask_wallet or mask_flop):
                if width-148 <= mouse[0] <= width-20 and height-148 <= mouse[1] <= height-20:
                    mask_wallet = True
                if 20 <= mouse[0] <= 148 and height-148 <= mouse[1] <= height-20:
                    return "map", game_state
                if width-148 <= mouse[0] <= width-20 and 20 <= mouse[1] <= 148:
                   return "departures", game_state
            elif event.type == pygame.MOUSEBUTTONDOWN and mask_wallet:
                if x <= mouse[0] <= x+120 and y <= mouse[1] <= y+56:
                    mask_wallet = False
            elif event.type == pygame.MOUSEBUTTONDOWN and mask_flop:
                for button in ticket_buttons:
                    if button.on_button(mouse):
                        game_state.wallet.buy_ticket(button.ticket)
                        mask_flop = False
                        game_state.need_flop = False

        
        # if mouse is hovered on a button it
        # moves down 5 pixels
        # Wallet Button
        if width-148 <= mouse[0] <= width-20 and height-148 <= mouse[1] <= height-20 and not (mask_wallet or mask_flop):
            screen.blit(wallet_img, (width-148, height-148+5))
        else:
            screen.blit(wallet_img, (width-148, height-148))

        # Map Button
        if 20 <= mouse[0] <= 148 and height-148 <= mouse[1] <= height-20 and not (mask_wallet or mask_flop):
            screen.blit(map_img, (20, height-15-148))
        else:
            screen.blit(map_img, (20, height-20-148))

        # Departures Button
        if width-148 <= mouse[0] <= width-20 and 20 <= mouse[1] <= 148 and not (mask_wallet or mask_flop):
            screen.blit(departres_img, (width-148, 25))
        else:
            screen.blit(departres_img, (width-148, 20))

        screen.blit(char_img, (800, 600))

        if mask_wallet:
            screen.blit(mask_img, (0,0))
            show_wallet(screen, mouse, game_state)

            x = 64
            y = height-144
            # Back Button
            if x <= mouse[0] <= x+120 and y <= mouse[1] <= y+56:
                screen.blit(close_img, (x, y+4))
                write_string(screen, "Close", x+20, y+20)
            else:
                screen.blit(close_img, (x, y))
                write_string(screen, "Close", x+20, y+16)
            

        if mask_flop:
            screen.blit(mask_img, (0,0))
            ticket_buttons = flop_overlay(screen, mouse, game_state)
            show_wallet(screen, mouse, game_state)

        screen.blit(clock_img, (10, 0))
        write_string(screen, f"{game_state.clock}", 50, 32)

        pygame.display.flip()
        game_state.tick()

        # print(clock.get_fps())
        clock.tick(30)

    pygame.quit()
