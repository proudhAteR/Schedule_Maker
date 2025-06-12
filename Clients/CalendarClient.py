from Clients.Client import Client


class CalendarClient(Client):
    def __init__(self):
        super().__init__('https://www.googleapis.com/auth/calendar')