import json
from entities.ticket import TransportType
from entities.time import generate_random_time

class Location:
    def __init__(self, id, x, y, name, station_types):
        self.id = id
        self.x = x
        self.y = y
        self.name = name
        self.station_types = station_types
        self.links = []
        self.departures = []

    def __str__(self):
        s = f"ID: {self.id}, Name: {self.name}, X: {self.x}, Y: {self.y}, Station Types: {self.station_types}, Links: "
        for c in self.links:
            s += f"Destination: {c[0]}, Connection: {c[1]}, "
        return s

class Connection:
    def __init__(self, distance, transportType):
        self.distance = distance
        self.transport_types = transportType

    def __str__(self):
        return f"Distance: {self.distance}"
    
class Destination:
    def __init__(self, destination, distance, transport, departure):
        self.destination = destination
        self.distance = distance
        self.transport = TransportType(transport)
        self.departure_time = departure
        match self.transport:
            case TransportType.PLANE: 
                self.time = distance * 1 + 120
            case TransportType.TRAIN:
                self.time = distance * 2
            case TransportType.BUS:
                self.time = distance * 5
            case TransportType.CAR: 
                self.time = distance * 3
            case TransportType.BOAT:
                self.time = distance * 8
            case _:
                self.time = distance
    
    def __str__(self):
        return f"Destination: {self.destination}, Distance: {self.distance}, Transport: {self.transport}, Time: {self.time}, Departure Time: {self.departure_time}"


class Map:
    def __init__(self, mapName):
        self.locationCount = 0
        self.locations = []
        self.location_name_to_id_map = {}
        self.map_name = mapName
        self.start_point = ""
        self.end_point = ""
        self.readMap(f"resources/maps/{mapName}.json")
        self.destinations = []
        self.init_destinations(self.start_point)
        

    def addLocation(self, x, y, name, station_types):
        new_loc = Location(self.locationCount, x, y, name, station_types)
        self.locations.append(new_loc)
        self.locationCount += 1
        self.location_name_to_id_map[name] = new_loc.id

    def linkLocations(self, primaryLocation, secondaryLocation, connection):
        self.locations[primaryLocation].links.append((secondaryLocation, connection))
        self.locations[secondaryLocation].links.append((primaryLocation, connection))


    def readMap(self, filePath):
        with open(filePath, "r") as mapfile:
            mapdata = json.load(mapfile)
            locations = mapdata['locations']
            connections = mapdata['connections']
            for l in locations:
                self.addLocation(l['x'], l['y'], l['name'], l['stationTypes'])
            
            for c in connections:
                first = self.location_name_to_id_map[c['first']]
                second = self.location_name_to_id_map[c['second']]
                self.linkLocations(first, second, Connection(c['distance'], c['transport_types']))
            self.start_point = mapdata["start_point"]
            self.end_point = mapdata["end_point"]

    def get_location_by_name(self, name):
        return self.locations[self.location_name_to_id_map[name]]

    def get_compatible_transport_modes(self, origin, destination):
        both = []
        for i in origin.station_types:
            if i in destination.station_types:
                both.append(i)
        return both

    def init_destinations(self, origin):
        locs = self.get_location_by_name(origin).links
        destinations = []
        for loc in locs:
            for d in loc[1].transport_types:
                departure_time = generate_random_time()
                destination = Destination(self.locations[loc[0]], loc[1].distance, d, departure_time)
                destinations.append(destination)
        self.destinations = sorted(destinations, key=lambda d: d.departure_time.get_total_minutes())

    def get_destinations(self, origin):
        return self.destinations
    
    def get_destination_names(self, origin):
        locs = self.get_location_by_name(origin).links
        destinations = set()
        for loc in locs:
            for _ in loc[1].transport_types:
                destinations.add(self.locations[loc[0]].name)
        return destinations

    

    def __str__(self):
        s = f"Start Point: {self.start_point}\n"
        for l in self.locations:
            s += f"{l}\n"
        return s


        
        