class user:
    def __init__(self, name_user, password):
        self.__name_user = name_user
        self.__password = name_user
        self.__soma_notas = 0
        self.__quantidade_de_notas = 0
        self.__nota = 0

    def addNota(self, new_nota):
        self.__nota_geral += new_nota
        self.__quantidade_de_notas += 1
        self.__nota = self.__soma_notas / self.__quantidade_de_notas 

    
    def getNota(self):
        if self.__quantidade_de_notas == 0:
            return "usuário ainda sem nota"
        return self.__nota
