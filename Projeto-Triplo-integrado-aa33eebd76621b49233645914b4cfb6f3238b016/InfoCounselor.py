class InfoCounselor:
    def __init__(self, nickname, socket, nota):
        self.nickname = nickname
        self.socket = socket
        self.nota = nota 
        

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

    def __le__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota <= outroObjeto.nota
    
    def __ge__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota >= outroObjeto.nota