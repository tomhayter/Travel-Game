import pygame
from util.load_image import get_logo_from_transport_type, get_ticket_img_from_type, import_image
from util.button import DepartButton, TicketButton
from util.font import write_string
from entities.time import minutes_to_time_string

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

color_brown = (150, 75, 0)

def departures_screen(screen, game_state):
    print("Move")
    width = screen.get_width()
    height = screen.get_height()

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, size=30)

    running = True
    title = "Departures"
    back = font.render("Back", True, (0, 0, 0))

    clock_img = import_image(f"resources/sprites/clock.png")
    dep_row_img = import_image(f"resources/sprites/departure_backing2.png")
    dep_row_down_img = import_image(f"resources/sprites/departure_backing2_down.png")
    wallet_img = import_image(f"resources/sprites/wallet.png")
    popup_distance_img = import_image("resources/sprites/popup_distance.png")

    departures = game_state.map.get_destinations(game_state.route[-1])
    departure_buttons = []

    tickets = []
    active_ticket = None
    key_pressed = None


    while running:
        # print("Game running")
        screen.fill((0, 0, 0))
        write_string(screen, title, 500, 30)
        mouse = pygame.mouse.get_pos()

        # Generate destinations
        next_dep = 0
        for i in range(len(departures)):
            if game_state.clock.datetime.before(departures[i].departure_time):
                next_dep = i
                break

        departure_buttons = []
        for i in range(min(7, len(departures[next_dep:]))):
            x = 1200
            y = 128 + i * 60
            dep = departures[next_dep+i]
            
            logo = get_logo_from_transport_type(dep.transport)
            if y <= mouse[1] <= y+56 and active_ticket != None:
                screen.blit(dep_row_down_img, (0, y))
            else:
                screen.blit(dep_row_img, (0, y))
            write_string(screen, dep.departure_time.get_time_string(), 20, y+16)
            screen.blit(logo, (180, y+8))
            write_string(screen, dep.destination.name, 260, y+16)
            write_string(screen, f"{dep.distance}km", 700, y+16)
            write_string(screen, f"{minutes_to_time_string(dep.time)}", 900, y+16)

            departure_buttons.append(DepartButton(dep.destination, dep.transport, dep.distance, dep.time, dep.departure_time, (0, y), (screen.get_width(), 56)))
        

        # pygame.draw.rect(screen, color_brown, [50, height-150, width-100, 150])
        screen.blit(wallet_img, (0, height-160))
        x = (width / 2) - (4*48) - 20
        y = height - 80 - 64
        for ticket in game_state.wallet.tickets:
            img = get_ticket_img_from_type(ticket.transport_type)
            if active_ticket != None:
                if active_ticket.ticket == ticket:
                    screen.blit(img, (active_ticket.bottom_corner[0], active_ticket.bottom_corner[1]))
                    continue

            if x <= mouse[0] <= x+96 and y <= mouse[1] <= y+128:
                screen.blit(img, (x, y-4))
                screen.blit(popup_distance_img, (x-18, y-68))
                write_string(screen, f"{ticket.distance}km", x-8, y-50)
            else:
                screen.blit(img, (x, y))
            tickets.append(TicketButton(ticket, (x, y), (96, 128)))
            x = x + 96 + 20

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
            
            if event.type == pygame.KEYUP:
                key_pressed = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if width-160 <= mouse[0] <= width-20 and 20 <= mouse[1] <= 60:
                    return "location", game_state
                for ticket in tickets:
                    if ticket.on_button(mouse):
                        active_ticket = ticket

            if event.type == pygame.MOUSEMOTION:
                if active_ticket != None:
                    active_ticket.bottom_corner = (active_ticket.bottom_corner[0] + event.rel[0], active_ticket.bottom_corner[1] + event.rel[1])

            if event.type == pygame.MOUSEBUTTONUP:
                if active_ticket != None:
                    for button in departure_buttons:
                        if button.on_button(mouse):
                            if game_state.valid_ticket_for_journey(active_ticket.ticket, button):
                                game_state.wallet.remove_ticket(active_ticket.ticket)
                                game_state.travel(button.destination, button.distance, button.transport_type, button.duration, button.departure_time, False)
                                if game_state.route[-1] == game_state.end_point:
                                    return "end", game_state
                                return "location", game_state
                active_ticket = None                    
        
        
        # if mouse is hovered on a button it
        # changes to lighter shade 
        if width-160 <= mouse[0] <= width-20 and 20 <= mouse[1] <= 60:
            pygame.draw.rect(screen,color_light,[width-160,20,140,40])
            
        else:
            pygame.draw.rect(screen,color_dark,[width-160,20,140,40])

        
        # superimposing the text onto our button
        screen.blit(back, (width-150,30))

        screen.blit(clock_img, (10, 0))
        write_string(screen, f"{game_state.clock}", 50, 32)

        pygame.display.flip()
        if key_pressed == pygame.K_t:
            game_state.tick(15)
        game_state.tick()
        clock.tick(30)

        
    
    pygame.quit()
