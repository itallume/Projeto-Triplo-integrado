import socket
import threading
lista_usuarios = {
    
    "fernando": "123"
}

class Server:
    def __init__(self, adress:str , porta:int):
        self.adress = adress
        self.port = porta
        
        
        
    def start_server(self):
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", self.port))
        server.listen()
        print(f"Servidor aguardando conexao na porta {self.port}")
        
        while True:
            self.aceitar_clientes(server)
            

    def aceitar_clientes(self, server):
        
        connection, end_client = server.accept()
        print(f"Conexão estabelecida com {end_client}")
        
        threading.Thread(target=self.clientComunication, args=(connection,)).start()
        
    def clientComunication(self, connection):
        
        while True:
            
            msg_client = connection.recv(1024).decode("utf-8").split(" ")
            
            
            # criar um while para o login e cadastro
            if msg_client[0] == "login":   # fazer a tentativa maxima de 10 login por nome de usuário                                                                       
                if msg_client[1] in lista_usuarios:
                    if lista_usuarios[msg_client[1]] ==  msg_client[2]:
                        connection.send("Login efetuado!".encode('utf-8')) 
                        continue
                    else:
                        connection.send("Usuário ou senha incorreto.".encode('utf-8'))
                        continue
                else:
                    connection.send("Usuário ou senha incorreto.".encode('utf-8'))
                    continue
            if msg_client[0] == "register":                                                                          
                if msg_client[1] in lista_usuarios:
                    connection.send("erro".encode('utf-8'))
                    continue
                lista_usuarios[msg_client[1]] = msg_client[2]
                connection.send("ok".encode('utf-8'))
                print(lista_usuarios)
                continue
                
                        
            if not msg_client:
                break
            print(f"Cliente: {msg_client}")
            
            response = input("Servidor: ")
            connection.send(response.encode('utf-8'))

        connection.close()
    
    def login():
        return ('''
            1 - Login
            2 - Signup    
        ''')    

        
    def menu():
        return('''
            Menu:
            1 - Receber conselhos (aconselhado)
            2 - Enviar conselhos (conselheiro)
            3 - Ver conselhos anteriores
            ''')


servidor = Server("0.0.0.0", 12345)
servidor.start_server()