class InfoCounselor:
    def __init__(self, nickname, socket, nota):
        self.__nickname = nickname
        self.__socket = socket
        self.__nota = nota #encapsulados!!!
        self.__notasArray = []

    @property
    def nickname(self):
        return self.__nickname
    
    @property
    def socket(self):
        return self.__socket
    
    @property
    def nota(self):
        return self.__nota
    
    @property
    def notasArray(self):
        return self.__notas

    def addNota(self, new_nota):
        self.__nota = self.__notasArray.append(new_nota)

    def calcular_media(self):
        if len(self.__notasArray) == 0:
            return 0
        return sum(self.__notasArray) / len(self.__notasArray)



    def __str__(self):
        return f"{self.nickname} - {self.nota}"

    def __eq__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota == outroObjeto.nota

    def __lt__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota < outroObjeto.nota
    
    def __gt__(self, outro_objeto):
        '''Método que possibilita comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota > outro_objeto.nota

    