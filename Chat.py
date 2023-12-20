class Chat:
    def __init__(self, assunto, intensidade):
        self.assunto = assunto
        self.intensidade = intensidade
        self.clients = []
        self.status = "desconectado"

    def addOnChat(self, nickname, socket):
        self.clients.append([nickname, socket])
        
    def getClients(self):
        return [self.clients[0][1], self.clients[1][1]]
    
    def changeStatus(self):
        if self.status == "desconectado":
            self.status = "ativo"
        else:
            self.status = "desconectado"
            
        return self.status