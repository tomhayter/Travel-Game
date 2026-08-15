WALLET_FULL = "Sorry, your wallet is full"
BROKE = "Sorry, not enough Money"
from entities.ticket import Ticket, TransportType, TicketPrice

default_tickets = [Ticket(TransportType.BUS, TicketPrice.FREE, 100, ""), Ticket(TransportType.BUS, TicketPrice.FREE, 200, ""), Ticket(TransportType.BUS, TicketPrice.FREE, 500, "")]

class Wallet:
    def __init__(self):
        self.tickets = default_tickets
        self.capacity = 5
        self.money = 1000

    def add_ticket(self, ticket):
        if len(self.tickets) >= self.capacity:
            raise Exception(WALLET_FULL)
        self.tickets.append(ticket)

    def remove_ticket(self, ticket_tbd):
        for ticket in self.tickets:
            if ticket == ticket_tbd:
                self.tickets.remove(ticket)

    def buy_ticket(self, ticket):
        if ticket.price.value > self.money:
            return Exception(BROKE)
        self.money = self.money - ticket.price.value
        self.add_ticket(ticket)
            