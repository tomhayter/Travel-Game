import pygame
from entities.ticket import TransportType

IMAGE_SCALE = 4

def import_image(filepath):
    im = pygame.image.load(filepath)
    return pygame.transform.scale_by(im, IMAGE_SCALE)

def get_ticket_img_from_type(transport_type):
    match transport_type:
        case TransportType.BUS:
            return import_image("resources/sprites/tickets/ticket_bus.png")
        case TransportType.PLANE:
            return import_image("resources/sprites/tickets/ticket_plane.png")
        case TransportType.TRAIN:
            return import_image("resources/sprites/tickets/ticket_train.png")
        case TransportType.CAR:
            return import_image("resources/sprites/tickets/ticket_demo_car.png")
        case TransportType.BOAT:
            return import_image("resources/sprites/tickets/ticket_boat.png")


def get_logo_from_transport_type(transport_type):
    match transport_type:
        case TransportType.PLANE:
            return import_image("resources/sprites/plane_logo.png")
        case TransportType.TRAIN:
            return import_image("resources/sprites/train_logo.png")
        case TransportType.BUS:
            return import_image("resources/sprites/bus_logo.png")
        case TransportType.CAR:
            return import_image("resources/sprites/car_logo.png")
        case TransportType.BOAT:
            return import_image("resources/sprites/boat_logo.png")

    match TransportType(transport_type):
        case TransportType.PLANE:
            return import_image("resources/sprites/plane_logo.png")
        case TransportType.TRAIN:
            return import_image("resources/sprites/train_logo.png")
        case TransportType.BUS:
            return import_image("resources/sprites/bus_logo.png")
        case TransportType.CAR:
            return import_image("resources/sprites/car_logo.png")
        case TransportType.BOAT:
            return import_image("resources/sprites/boat_logo.png")