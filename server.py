import socket
import threading
from ChainingHashTableProblema import ChainingHashTable
from User import User
from ListaEncadeada import Lista
from Chat import Chat
import time
class Server:
    def __init__(self, adress:str , porta:int):
        self.adress = adress
        self.port = porta
        self.usersHashTable = ChainingHashTable(20)
        self.chats = ChainingHashTable(20)
        self.undecidedList = Lista()
        self.arvore = []
        
        
    def start_server(self):
        
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.bind(("0.0.0.0", self.port))
        clientSocket.listen()
        print(f"Servidor aguardando conexao na porta {self.port}")
        
        while True:
            self.aceitar_clientes(clientSocket)
            

    def aceitar_clientes(self, clientSocket):
        
        connection, end_client = clientSocket.accept()
        print(f"Conexão estabelecida com {end_client}")
        
        threading.Thread(target=self.clientComunication, args=(connection,)).start()
        
    def clientComunication(self, connection):
        while True:
            
            msg_client = connection.recv(1024).decode("utf-8").split(" ")
            # criar um while para o login e cadastro
            if msg_client[0] == "login":   # fazer a tentativa maxima de 10 login por nome de usuário    
                for i in range(10): 
                    if i == 9:
                        break                                                                 
                    if self.usersHashTable.contains(msg_client[1]):
                            #retorna um objeto User
                        if self.usersHashTable.get(msg_client[1]).confirmPassword(msg_client[2]):  # com o metodo confirmPassword da classe User, faz a confirmação da senha
                            connection.send("Login efetuado!".encode('utf-8')) # subtituir por codigos
                            UserObject = self.usersHashTable.get(msg_client[1])
                            login = True
                            break
                        else:
                            connection.send("Usuário ou senha incorreto. 2".encode('utf-8'))  # subtituir por codigos
                            msg_client = connection.recv(1024).decode("utf-8").split(" ") 
                            continue
                    else:
                        connection.send("Usuário ou senha incorreto. 1".encode('utf-8')) # subtituir por codigos
                        msg_client = connection.recv(1024).decode("utf-8").split(" ") 
                        continue
                if login:
                    connection.send("muitas tentativas de login, tente mais tarde".encode('utf-8'))
                    connection.close()
                    return
            
            if msg_client[0] == "register":   
                                                                                       
                if self.usersHashTable.contains(msg_client[1]): # verifica se já existe algum usuário com o nome de usuário desejado
                    connection.send("error".encode('utf-8')) # subtituir por codigos
                    continue
                 #usar lock aqui!!!
                UserObject = User(msg_client[1], msg_client[2])
                self.usersHashTable.put(msg_client[1], UserObject)
                
                connection.send("210 OK".encode('utf-8')) # subtituir por codigos
                self.usersHashTable.displayTable()
                print()
                continue
                
            if msg_client[0] == "type":
                if msg_client[1] == "undecided":
                    # self.undecidedList.inserir(self.undecidedList.tamanho + 1, )
                    newChat = Chat(msg_client[2], msg_client[3])
                    newChat.addOnChat(UserObject.nickname, connection)
                    self.chats.put(UserObject.nickname, newChat)
                    threading.Thread(target= self.matchClients, args=()).start()
                if msg_client[1] == "counselor":    
                    self.arvore.append([UserObject.nickname, connection])
                    
            if not msg_client:
                break
            print(f"Cliente: {msg_client}")
            
            response = input("Servidor: ")
            connection.send(response.encode('utf-8'))

        connection.close()
        
    def matchClients(self):
        while len(self.chats) != 0:
            for chat in self.chats.values():
                while len(self.arvore) == 0:
                    time.sleep(1)
                chat.addOnChat(self.arvore[0][0], self.arvore[0][1])
                chat_clients = chat.getClients()
                for connection in chat_clients:
                    connection.send(f"CONECTADOS AO CHAT\nASSUNTO DO CHAT: {chat.assunto}".encode('utf-8'))
                
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