import socket
import threading
from ChainingHashTableProblema import ChainingHashTable
from User import User

class Server:
    def __init__(self, adress:str , porta:int):
        self.adress = adress
        self.port = porta
        self.usersHashTable = ChainingHashTable(20)
        
        
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
                if self.usersHashTable.contains(msg_client[1]):
                           #retorna um objeto User
                    if self.usersHashTable.get(msg_client[1]).confirmPassword(msg_client[2]):  # com o metodo confirmPassword da classe User, faz a confirmação da senha
                        connection.send("Login efetuado!".encode('utf-8')) # subtituir por codigos
                        continue
                    else:
                        connection.send("Usuário ou senha incorreto. 2".encode('utf-8'))  # subtituir por codigos
                        continue
                else:
                    connection.send("Usuário ou senha incorreto. 1".encode('utf-8')) # subtituir por codigos
                    continue
                
            if msg_client[0] == "register":   
                                                                                       
                if self.usersHashTable.contains(msg_client[1]): # verifica se já existe algum usuário com o nome de usuário desejado
                    connection.send("error".encode('utf-8')) # subtituir por codigos
                    continue
                
                objectUser = User(msg_client[1], msg_client[2])
                self.usersHashTable.put(msg_client[1], objectUser)
                
                connection.send("ok".encode('utf-8')) # subtituir por codigos
                self.usersHashTable.displayTable()
                print()
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