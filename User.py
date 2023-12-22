class User:
    def __init__(self, nickname, password):
        self.__nickname = nickname
        self.__password = password
        self.__soma_notas = 10  # inicia com 10
        self.__quantidade_de_notas = 0
        self.__nota = 10
        self.__chat = None 
        
    @property
    def nickname(self):
        return self.__nickname
    
    @property
    def nota(self):
        return self.__nota
    
    @property
    def chat(self):
        return self.__chat
    
    @property
    def status(self):
        return self.__status

    @chat.setter
    def chat(self, newchat):
        self.__chat = newchat
    
    def addNota(self, new_nota):
        self.__soma_notas += new_nota
        self.__quantidade_de_notas += 1
        self.__nota = self.__soma_notas / self.__quantidade_de_notas 
        return self.__nota

    def confirmPassword(self, password):
        if password == self.__password:
            return True
        
    def __eq__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota == outroObjeto.nota

    def __lt__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota < outroObjeto.nota
    
    def __gt__(self, outro_objeto):
        '''Método que possibilita comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota > outro_objeto.nota
