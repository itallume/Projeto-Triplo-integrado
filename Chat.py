class Chat:
    def __init__(self, assunto:str, intensidade:int):
        self.assunto = assunto
        self.intensidade = intensidade
        self.clients = []


    def addOnChat(self, nickname, socket):
        """O método `addOnChat` adiciona um novo participante à lista de clientes de um chat."""
        self.clients.append([nickname, socket])
        
    def getClients(self:list):
        """O método `getClients` retorna a lista de clientes atualmente presentes no chat."""
        usersOnChat = []
        for user in self.clients:
            usersOnChat.append(user)
        return usersOnChat
    