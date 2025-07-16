from Infrastructure.Clients.Client import Client


class GoogleClient(Client):
    def __init__(self, name: str):
        api_pth: str = 'https://www.googleapis.com/auth/'
        super().__init__(api_pth + name)
