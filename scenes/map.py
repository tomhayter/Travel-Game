import pygame
from util.load_image import import_image, IMAGE_SCALE, get_logo_from_transport_type
from math import sqrt
from util.camera import Camera
from util.font import write_string


# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

def dashed_line(start, end):
    total_x = end[0] - start[0]
    total_y = end[1]- start[1]
    magnitude = sqrt(total_x**2 + total_y**2)
    norm_x = total_x / magnitude
    norm_y = total_y / magnitude
    points = []

    num_dashes = 0
    if norm_x != 0:
        num_dashes = total_x / (10 * norm_x)
    else:
        num_dashes = total_y / (10 * norm_y)

    points.append(start)
    for _ in range(int(num_dashes)):
        next_point = (points[-1][0] + 10 * norm_x, points[-1][1] + 10 * norm_y)
        points.append(next_point)
    
    points.append(end)
    return points




def map_screen(screen, game_state):
    print("Map")
    width = screen.get_width()
    height = screen.get_height()
    map_img = import_image(f"resources/sprites/maps/{game_state.map.map_name}.png")
    marker_img = import_image(f"resources/sprites/map_marker.png")
    marker_here = import_image(f"resources/sprites/map_marker_here.png")
    marker_been = import_image(f"resources/sprites/map_marker_been.png")
    marker_end = import_image(f"resources/sprites/map_marker_end.png")
    clock_img = import_image(f"resources/sprites/clock.png")
    helper_img = import_image(f"resources/sprites/map_location_helper.png")

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, size=30)

    running = True
    back = font.render("Back", True, (0, 0, 0))

    possible_destinations = game_state.map.get_destinations(game_state.route[-1])
    current_loc = game_state.get_current_loc()

    camera_loc = ((-1*IMAGE_SCALE*current_loc.x) + (width/2), (-1*IMAGE_SCALE*current_loc.y) + (height/2))
    print(camera_loc)
    camera = Camera(camera_loc)
    camera_key_pressed = None

    while running:
        # print("Game running")

        camera_loc = camera.update_camera_loc(camera_key_pressed, map_img.get_size(), screen.get_size())
        camera.display(screen, map_img, (0,0))
        # screen.blit(map_img, camera_loc)


        current_loc_x = IMAGE_SCALE*(current_loc.x-3)
        current_loc_y = IMAGE_SCALE*(current_loc.y-3)
        for possible in possible_destinations:
            poss_x = IMAGE_SCALE*(possible.destination.x)
            poss_y = IMAGE_SCALE*(possible.destination.y)
            dashes = dashed_line((current_loc_x+(IMAGE_SCALE*3), current_loc_y+(IMAGE_SCALE*3)), (poss_x, poss_y))
            last_painted = False
            for i in range(len(dashes)-1):
                if last_painted:
                    last_painted = False
                    continue
                last_painted = True
                camera.draw_line(screen, (160, 160, 160), dashes[i], dashes[i+1], IMAGE_SCALE)

        for i in range(len(game_state.route)-1):
            start = game_state.map.get_location_by_name(game_state.route[i])
            end = game_state.map.get_location_by_name(game_state.route[i+1])
            camera.draw_line(screen, (0, 0, 0), (IMAGE_SCALE*start.x, IMAGE_SCALE*start.y), (IMAGE_SCALE*end.x, IMAGE_SCALE*end.y), IMAGE_SCALE)

        display_helper = False
        helper_x = 0
        helper_y = 0
        helper_place = ""
        helper_text = ""
        helper_transport_modes = []
        for loc in game_state.map.locations:
            loc_img = marker_img
            if loc.name in game_state.route:
                loc_img = marker_been
            if game_state.end_point == loc.name:
                loc_img = marker_end
            if current_loc.name == loc.name:
                loc_img = marker_here

            loc_x = IMAGE_SCALE*(loc.x-3)
            loc_y = IMAGE_SCALE*(loc.y-3)
            camera.display(screen, loc_img, (loc_x, loc_y))

            # Show place description on hover
            if camera.get_img_rect(marker_img, (loc_x, loc_y)).collidepoint(pygame.mouse.get_pos()):
                display_helper = True
                helper_place = loc.name
                helper_x = loc_x
                helper_y = loc_y
                helper_transport_modes = loc.station_types

                helper_text = f"DISTANCE: Xkm"
                if (current_loc.name == loc.name):
                    helper_text = "YOU ARE HERE"


                

        if display_helper:
            camera.display(screen, helper_img, (helper_x - (10 * IMAGE_SCALE), helper_y  - IMAGE_SCALE - helper_img.get_height()))
            camera.write_string(screen, helper_place, (helper_x, helper_y - (helper_img.get_height() - (5*IMAGE_SCALE))))
            camera.write_string(screen, helper_text, (helper_x, helper_y - (helper_img.get_height() - (12*IMAGE_SCALE))))
            x_offset = 0
            for poss_transport in helper_transport_modes:
                t_image = get_logo_from_transport_type(poss_transport)
                camera.display(screen, t_image, (helper_x + x_offset, helper_y  - (helper_img.get_height() - (20*IMAGE_SCALE))))
                x_offset += (t_image.get_width() + (IMAGE_SCALE * 3))
                    

        
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                camera_key_pressed = event.key
            
            if event.type == pygame.KEYUP:
                camera_key_pressed = None


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
