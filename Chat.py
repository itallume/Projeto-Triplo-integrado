class Chat:
    def __init__(self, assunto, intensidade):
        self.assunto = assunto
        self.intensidade = intensidade
        self.clients = []
    
    def addOnChat(self, nickname, socket):
        self.clients.append([nickname, socket])
        
    def getClients(self):
        return [self.clients[0][1], self.clients[1][1]]