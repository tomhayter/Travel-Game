class Button:
    def __init__(self, bottom_corner, size):
        self.bottom_corner = bottom_corner
        self.size = size
        self.top_corner = (bottom_corner[0] + size[0], bottom_corner[1] + size[1])

    def on_button(self, mouse_pos):
        if self.top_corner[0] >= mouse_pos[0] >= self.bottom_corner[0] and self.top_corner[1] >= mouse_pos[1] >= self.bottom_corner[1]:
            return True
        return False
    
class TicketButton(Button):
    def __init__(self, ticket, bottom_corner, size):
        self.ticket = ticket
        super().__init__(bottom_corner, size)

class DepartButton(Button):
    def __init__(self, destination, transport, distance, duration, departure_time, bottom_corner, size):
        self.destination = destination
        self.transport_type = transport
        self.distance = distance
        self.duration = duration
        self.departure_time = departure_time
        super().__init__(bottom_corner, size)