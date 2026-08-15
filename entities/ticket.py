from enum import Enum
import random
import time

class Ticket:
    def __init__(self, transport_type, price, distance, restriction):
        self.transport_type = transport_type
        self.price = price
        self.distance = distance
        self.restriction = restriction


class TransportType(Enum):
    PLANE = 1
    BOAT = 2
    TRAIN = 3
    BUS = 4
    CAR = 5

class TicketPrice(Enum):
    FREE = 0
    CHEAP = 20
    MIDRANGE = 50
    EXPENSIVE = 100

POSSIBLE_DISTANCES=[50, 100, 200, 300, 400, 500]

def generate_flop():
    flop = []
    flop.append(generate_random_ticket(TicketPrice.CHEAP))
    flop.append(generate_random_ticket(TicketPrice.MIDRANGE))
    flop.append(generate_random_ticket(TicketPrice.EXPENSIVE))
    return flop

def generate_random_ticket(price):
    random.seed(time.time() * 1000)
    match price:
        case TicketPrice.CHEAP:
            return Ticket(TransportType(random.randint(2, 4)),
                          TicketPrice.CHEAP,
                          POSSIBLE_DISTANCES[random.randint(0, 2)],
                          None)
        case TicketPrice.MIDRANGE:
            return Ticket(TransportType(random.randint(1, 4)),
                          TicketPrice.MIDRANGE,
                          POSSIBLE_DISTANCES[random.randint(1, 4)],
                          None)
        case TicketPrice.EXPENSIVE:
            return Ticket(TransportType(random.randint(1, 4)),
                          TicketPrice.EXPENSIVE,
                          POSSIBLE_DISTANCES[random.randint(3, 5)],
                          None)