from entities.map import Map
from entities.wallet import Wallet
from entities.time import Clock
from entities.ticket import generate_flop

class GameState:
    def __init__(self, mapName):
        self.map = Map(mapName)
        self.wallet = Wallet()
        self.route = [self.map.start_point]
        self.end_point = self.map.end_point
        self.statistics = GameStatistics()
        self.ticks = 0
        self.clock = Clock()
        self.need_flop = True
        self.flop = []
        self.new_flop()

    def get_current_loc(self):
        return self.map.get_location_by_name(self.route[-1])

    def travel(self, destination, distance, transport_type, duration, departure_time, tomorrow):
        self.route.append(destination.name)
        hour = duration // 60
        minute = duration % 60
        self.clock.set_time(departure_time, tomorrow)
        self.clock.pass_time(hour, minute)
        self.map.init_destinations(destination.name)
        self.statistics.distance_travelled += distance
        self.statistics.transport_modes_used.add(transport_type)
        self.statistics.locations_travelled.add(destination.name)
        self.need_flop = True
        self.new_flop()
        
    def valid_ticket_for_journey(self, ticket, journey):
        if ticket.transport_type != journey.transport_type:
            print(f"Invalid ticket: wrong type. Got: {ticket.transport_type}, needed: {journey.transport_type}")
            return False
        if ticket.distance < journey.distance:
            print(f"Invalid ticket: distance too short. Got: {ticket.distance}, needed: {journey.distance}")
            return False
        return True

    def tick(self, num_ticks=1):
        self.ticks += num_ticks
        if self.ticks >= 15:
            self.clock.tick()
            self.ticks = 0
            # print(self.clock)

    def new_flop(self):
        self.flop = generate_flop()

    def get_score(self):
        score = 0
        score += self.statistics.distance_travelled // 10
        score += len(self.statistics.transport_modes_used) * 100
        score += len(self.statistics.locations_travelled) * 25
        score += self.clock.datetime.day * 10
        return score


class GameStatistics:
    def __init__(self):
        self.distance_travelled = 0
        self.transport_modes_used = set()
        self.locations_travelled = set()

