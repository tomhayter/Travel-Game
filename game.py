from scenes import departures, flop, location, map, menu, wallet, endgame
import pygame
from util.font import load_alphabet

def start():
    load_alphabet()
    game_state = None
    scene = "menu"
    running = True
    pygame.init()
    # screen resolution
    res = (320, 180)
    res = (1920, 1080)
    res = (1280, 720)
    # screen = pygame.display.set_mode(res, pygame.FULLSCREEN)
    screen = pygame.display.set_mode(res)

    while running:
        match scene:
            case "menu":
                scene, game_state = menu.menu(screen)
            case "wallet":
                scene, game_state = wallet.wallet_screen(screen, game_state)
            case "map":
                scene, game_state = map.map_screen(screen, game_state)
            case "departures":
                scene, game_state = departures.departures_screen(screen, game_state)
            case "flop":
                scene, game_state = flop.flop_screen(screen, game_state)
            case "location":
                scene, game_state = location.location_scene(screen, game_state)
            case "end":
                scene, game_state = endgame.end_screen(screen, game_state)
            
            




if __name__ == "__main__":
    # print("Name is main")
    start()
