import pygame
from entities.ticket import generate_flop, TicketPrice
from util.load_image import get_ticket_img_from_type, import_image
from util.button import TicketButton
from util.font import write_string

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

coin_img = import_image("resources/sprites/coin.png")
flop_overlay_img = import_image("resources/sprites/flop_background.png")
popup_distance_img = import_image("resources/sprites/popup_distance.png")

def flop_overlay(screen, mouse, game_state):
    flop = game_state.flop
    ticket_buttons = []
    width = screen.get_width()
    height = screen.get_height()


    screen.blit(flop_overlay_img, (0, 200))

    write_string(screen, "Pick a Ticket", 500, 240)

    x = (width / 2) - (4*48) - 20
    y = (height / 2) - 64
    for i in range(3):
        ticket = flop[i]
        img = get_ticket_img_from_type(ticket.transport_type)

        if x <= mouse[0] <= x+96 and y <= mouse[1] <= y+128:
            screen.blit(img, (x, y-4))
            screen.blit(popup_distance_img, (x-18, y-68))
            write_string(screen, f"{ticket.distance}km", x-8, y-50)
        else:
            screen.blit(img, (x, y))
        ticket_buttons.append(TicketButton(ticket, (x, y), (96, 128)))
        price_y = y + 148
        price_x = x
        screen.blit(coin_img, (price_x, price_y))
        price_x += 32
        price_y += 10
        write_string(screen, f" {ticket.price.value}", price_x, price_y)

        x = x + 96 + 20

    return ticket_buttons

def flop_screen(screen, game_state):
    print("Pick a Ticket")
    width = screen.get_width()
    height = screen.get_height()

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, size=30)

    coin_img = import_image("resources/sprites/coin.png")
    clock_img = import_image(f"resources/sprites/clock.png")

    running = True
    title = "Pick a Ticket"
    flop = generate_flop()

    ticket_buttons = []

    while running:
        screen.fill((102, 204, 0))
        
        text = font.render(title, True, (0, 0, 0))
        screen.blit(text, (300, 30))
        mouse = pygame.mouse.get_pos()

        x = (width / 2) - (4*48) - 20
        y = (height / 2) - 64
        for i in range(3):
            ticket = flop[i]
            img = get_ticket_img_from_type(ticket.transport_type)

            if x <= mouse[0] <= x+96 and y <= mouse[1] <= y+128:
                screen.blit(img, (x, y-5))
            else:
                screen.blit(img, (x, y))
            ticket_buttons.append(TicketButton(ticket, (x, y), (96, 128)))
            price_y = y + 148
            price_x = x
            screen.blit(coin_img, (price_x, price_y))
            price_x += 40
            price_y += 10
            price = font.render(f"  {ticket.price.value}", True, (0, 0, 0))
            screen.blit(price, (price_x, price_y))

            x = x + 96 + 20
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if width-160 <= mouse[0] <= width-20 and height-60 <= mouse[1] <= height-20:
                    return "location", game_state
                
                for button in ticket_buttons:
                    if button.on_button(mouse):
                        game_state.wallet.buy_ticket(button.ticket)
                        return "location", game_state


        screen.blit(clock_img, (10, 0))
        write_string(screen, f"{game_state.clock}", 50, 32)
        pygame.display.flip()
        # print(clock.get_fps())
        game_state.tick()
        clock.tick(30)

        
    
    pygame.quit()
