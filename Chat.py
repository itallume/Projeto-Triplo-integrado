class Chat:
    def __init__(self, assunto:str, intensidade:int):
        self.assunto = assunto
        self.intensidade = intensidade
        self.clients = []
        self.status = "desconected"
        self.Indeciso = None
        self.conselheiro = None

    def addOnChat(self, nickname, socket):
        self.clients.append([nickname, socket])
        
    def getClients(self):
        usersOnChat = []
        for user in self.clients:
            usersOnChat.append(user)
        return usersOnChat
    
    def changeStatus(self):
        if self.status == "desconected":
            self.status = "active"
        else:
            self.status = "desconected"
            
        return self.status