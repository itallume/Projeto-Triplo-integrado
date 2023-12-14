class User:
    def __init__(self, nickname, password):
        self.__nickname = nickname
        self.__password = password
        self.__soma_notas = 0
        self.__quantidade_de_notas = 0
        self.__nota = 0
        self.__chat = None #ISSO É PROVISÓRIO, APENAS PARA TESTE
        
    @property
    def nickname(self):
        return self.__nickname
    
    @property
    def rate(self):
        return self.__nota
    
    @property
    def chat(self):
        return self.__chat
    
    @chat.setter
    def chat(self, newchat):
        self.__chat = newchat
    
    def addNota(self, new_nota):
        self.__nota_geral += new_nota
        self.__quantidade_de_notas += 1
        self.__nota = self.__soma_notas / self.__quantidade_de_notas 

    def confirmPassword(self, password):
        if password == self.__password:
            return True
