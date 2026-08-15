import pygame
from util.load_image import get_ticket_img_from_type, import_image
from util.font import write_string

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

coin_img = import_image("resources/sprites/coin.png")
wallet_img = import_image(f"resources/sprites/wallet.png")
popup_distance_img = import_image("resources/sprites/popup_distance.png")

def show_wallet(screen, mouse, game_state):
    width = screen.get_width()
    height = screen.get_height()
    screen.blit(wallet_img, (0, height-160))
    x = (width / 2) - (4*48) - 20
    y = height - 80 - 64
    write_string(screen, "Balance", width-64-136, height-124)
    screen.blit(coin_img, (width-64-136, height-64))
    write_string(screen, f"{game_state.wallet.money}", width-64-136+40, height-64+10)
    for ticket in game_state.wallet.tickets:
        img = get_ticket_img_from_type(ticket.transport_type)

        if x <= mouse[0] <= x+96 and y <= mouse[1] <= y+128:
            screen.blit(img, (x, y-4))
            screen.blit(popup_distance_img, (x-18, y-68))
            write_string(screen, f"{ticket.distance}km", x-8, y-50)
        else:
            screen.blit(img, (x, y))
        x = x + 96 + 20


def wallet_screen(screen, game_state):
    print("Wallet")
    width = screen.get_width()
    height = screen.get_height()

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, size=30)

    coin_img = import_image("resources/sprites/coin.png")
    clock_img = import_image(f"resources/sprites/clock.png")

    running = True
    title = "Wallet"
    back = font.render("Back", True, (0, 0, 0))

    while running:
        # print("Game running")
        screen.fill((102, 204, 0))
        
        text = font.render(title, True, (0, 0, 0))
        screen.blit(text, (300, 30))

        mouse = pygame.mouse.get_pos()

        # Money
        price_y = 100
        price_x = width/2 - 20
        screen.blit(coin_img, (price_x, price_y))
        price_x += 40
        price = font.render(f"  {game_state.wallet.money}", True, (0, 0, 0))
        screen.blit(price, (price_x, price_y+10))

        
        x = (width / 2) - (4*48) - 20
        y = (height / 2) - 64
        for ticket in game_state.wallet.tickets:
            img = get_ticket_img_from_type(ticket.transport_type)

            if x <= mouse[0] <= x+96 and y <= mouse[1] <= y+128:
                screen.blit(img, (x, y-5))
            else:
                screen.blit(img, (x, y))
            x = x + 96 + 20
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if width-160 <= mouse[0] <= width-20 and height-60 <= mouse[1] <= height-20:
                    return "location", game_state
        
        # if mouse is hovered on a button it
        # changes to lighter shade 
        if width-160 <= mouse[0] <= width-20 and height-60 <= mouse[1] <= height-20:
            pygame.draw.rect(screen,color_light,[width-160,height-60,140,40])
            
        else:
            pygame.draw.rect(screen,color_dark,[width-160,height-60,140,40])
        
        # superimposing the text onto our button
        screen.blit(back, (width-150,height-50))

        screen.blit(clock_img, (10, 0))
        write_string(screen, f"{game_state.clock}", 50, 32)

        pygame.display.flip()
        game_state.tick()
        clock.tick(30)

        
    
    pygame.quit()
