import socket
import threading
from ChainingHashTableProblema import ChainingHashTable
from User import User
from Chat import Chat
import time
class Server:
    def __init__(self, adress:str , porta:int):
        self.adress = adress
        self.port = porta
        self.usersHashTable = ChainingHashTable(20)
        self.chats = ChainingHashTable(20)
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
            
            msg_client = connection.recv(4096).decode("utf-8").split(" ")
            # criar um while para o login e cadastro
            if msg_client[0] == "login":   # fazer a tentativa maxima de 10 login por nome de usuário    
                for i in range(10): 
                    if i == 9:
                        break                                                                 
                    if self.usersHashTable.contains(msg_client[1]):
                            #retorna um objeto User
                        if self.usersHashTable.get(msg_client[1]).confirmPassword(msg_client[2]):  # com o metodo confirmPassword da classe User, faz a confirmação da senha
                            connection.send("200".encode('utf-8')) # subtituir por codigos
                            UserObject = self.usersHashTable.get(msg_client[1])
                            login = True
                            break
                        else:
                            connection.send("Usuário ou senha incorreto. 2".encode('utf-8'))  # subtituir por codigos
                            msg_client = connection.recv(4096).decode("utf-8").split(" ") 
                            continue
                    else:
                        connection.send("Usuário ou senha incorreto. 1".encode('utf-8')) # subtituir por codigos
                        msg_client = connection.recv(4096).decode("utf-8").split(" ") 
                        continue
                if login:
                    connection.send("muitas tentativas de login, tente mais tarde".encode('utf-8'))
                    connection.close()
                    return
                break
            if msg_client[0] == "register":   
                                                                                       
                if self.usersHashTable.contains(msg_client[1]): # verifica se já existe algum usuário com o nome de usuário desejado
                    connection.send("211".encode('utf-8')) # subtituir por codigos
                    continue
                 #usar lock aqui!!!
                UserObject = User(msg_client[1], msg_client[2])
                self.usersHashTable.put(msg_client[1], UserObject)
                connection.send("210".encode('utf-8')) # subtituir por codigos
                self.usersHashTable.displayTable()
                print()
                break
            
        while True:
            msg_client = connection.recv(4096).decode("utf-8").split("&")
            if msg_client[0] == "type":
                if msg_client[1] == "undecided":
                    newChat = Chat(msg_client[2], msg_client[3])  # cria um objeto chat com o assunto e a intensidade
                    newChat.addOnChat(UserObject.nickname, connection) # adiciona o menbro no chat
                    chat = newChat
                        # usar lock
                    self.chats.put(UserObject.nickname, newChat) # adicona o chat na ht de chats 
                    threading.Thread(target= self.matchClients, args=()).start()
                    break
                
                if msg_client[1] == "counselor":    
                    self.arvore.append([UserObject.nickname, connection])
                    # fazer as de solicitações de escolha de chat para o conselheiro 
                    while UserObject.chat is None:
                        time.sleep(0.2)
                    chat = UserObject.chat
                    break
        
        while True: 
            msg_client = connection.recv(4096).decode("utf-8").split("&") # receber a mensagem do cliente e separar o comando do texto
            print(msg_client) 
            if msg_client[0] == "msg":

                if msg_client[1].lower() == 'exit':
                    print("Desconectado")
                    response = '250'
                    for participants in chat.getClients():
                        participants.send(response.encode('utf-8')) #talvez cause bug
                        connection.close()
                        #PRECISA PARAR A THREAD
                    break
        

                for participants in chat.getClients():
                    print("socket: ", participants)
                    participants.send(f"txt&{UserObject.nickname}: {msg_client[1]}".encode('utf-8'))  


                
                 

        
    def matchClients(self):
        while len(self.chats) != 0:
            for chat in self.chats.values():
                if chat.status == "ativo": continue
                while len(self.arvore) == 0:
                    time.sleep(0.2)
                chat.addOnChat(self.arvore[0][0], self.arvore[0][1]) # fazer a busca na arvore de um um conselheiro 
                chat_clients = chat.getClients()
                chat.changeStatus()
                self.usersHashTable.get(self.arvore[0][0]).chat = chat
                for connection in chat_clients:
                    connection.send(f"200&CONECTADO!\nASSUNTO DO CHAT: {chat.assunto}".encode('utf-8'))
                
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
# servidor.usersHashTable.put("itallo" ,User("itallo", "123"))
# servidor.usersHashTable.put("paulo" ,User("paulo", "123"))
servidor.start_server()
