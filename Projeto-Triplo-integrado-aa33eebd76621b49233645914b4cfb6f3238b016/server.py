import socket
import threading
from ChainingHashTableProblema import ChainingHashTable
from BinarySearchTree import BinarySearchTree
from User import User
from Chat import Chat
import time
from InfoCounselor import InfoCounselor


class Server:
    def __init__(self, adress:str , porta:int):
        self.adress = adress
        self.port = porta
        self.usersHashTable = ChainingHashTable(20)
        self.AllChats = ChainingHashTable(20)
        self.arvore = BinarySearchTree()
        self.MinNote = None
        self.Lock = threading.Lock()
        
    def setDictionary(self):
        """ Atribui ao atributo MinNote da classe o dicionário que
            contém a nota minima para entrar em um chat
            com base nas intensidades 1, 2 e 3.
            Onde:
                1 = Intensidade baixa 
                2 = Intensidade média
                3 = Intendsidade alta
        """
        self.MinNote = {
            1: 0,
            2: 3,
            3: 6
        }
        
    def start_server(self):
        self.setDictionary()
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
        """Metodo que contem todos os meios de comunicação com o cliente"""
        while True:  
                try:   
                    msg_client = connection.recv(4096).decode("utf-8").split(" ")
                    # criar um while para o login e cadastro
                    if msg_client[0] == "login":   # fazer a tentativa maxima de 10 login por nome de usuário 
                        login = False   
                        for i in range(99999): 
                            if i < 999999:
                                break                                                                 
                            if self.usersHashTable.contains(msg_client[1]):
                                    #retorna um objeto User
                                if self.usersHashTable.get(msg_client[1]).confirmPassword(msg_client[2]):  # com o metodo confirmPassword da classe User, faz a confirmação da senha
                                    connection.send("200".encode('utf-8')) # subtituir por codigos
                                    UserObject = self.usersHashTable.get(msg_client[1])
                                    login = True
                                    break
                                else:
                                    connection.send("201".encode('utf-8'))  # subtituir por codigos
                                    msg_client = connection.recv(4096).decode("utf-8").split(" ")
                                    continue
                            else:
                                connection.send("201".encode('utf-8')) # subtituir por codigos
                                msg_client = connection.recv(4096).decode("utf-8").split(" ") 
                                continue
                        if login == False:
                            connection.send("299".encode('utf-8')) #Enviar codigo
                            connection.close()
                            return
                        break
                    
                 #Enviar codigo
                    if msg_client[0] == "register":   
                                                             
                        if self.usersHashTable.contains(msg_client[1]): # verifica se já existe algum usuário com o nome de usuário desejado
                            print("teste")
                            connection.send("211".encode('utf-8')) # subtituir por codigos
                            continue
                        
                        UserObject = User(msg_client[1], msg_client[2])
                        with self.Lock:
                            self.usersHashTable.put(msg_client[1], UserObject) # abre o server
                        connection.send("210".encode('utf-8')) # subtituir por codigos
                        self.usersHashTable.displayTable()
                        print()
                        break
             #Enviar codigo ABRE ABER ABRE ABRE manda paulo ir fazendo os SUPER COMENTARIOS AI DOCUEMNTACAO
                except ConnectionResetError as e:
                    print(f"Erro de conexão: {e}")
                    connection.send("555".encode('utf-8')) #Enviar codigo
                    
                    
            
        while True:
            try:
                msg_client = connection.recv(4096).decode("utf-8").split("&")
                if msg_client[0] == "type":
                    if msg_client[1] == "undecided":
                        newChat = Chat(msg_client[2], int(msg_client[3]))# cria um objeto chat com o assunto e a intensidade
                    
                        newChat.addOnChat(UserObject.nickname, connection) # adiciona o menbro no chat
                        chat = newChat
                            # usar lock
                        with self.Lock:    
                            self.AllChats.put(UserObject.nickname, newChat) # adicona o chat na ht de chats 
                        threading.Thread(target= self.matchClients, args=(chat,)).start()
                        break
                    
                    if msg_client[1] == "counselor": 
                        counselor = InfoCounselor(UserObject.nickname, connection, UserObject.nota)
                        with self.Lock:
                            self.arvore.add(counselor)
                        # fazer as de solicitações de escolha de chat para o conselheiro 
                        while UserObject.chat is None:
                            time.sleep(0.2)
                        chat = UserObject.chat # mandar a solicitação de chat aqui
                        break
            except ConnectionResetError as e:
                print(f"Erro de conexão: {e}")
                connection.send("555".encode('utf-8')) #Enviar codigo
                
        while True: 
            try:
                msg_client = connection.recv(4096).decode("utf-8").split("&") # receber a mensagem do cliente e separar o comando do texto
                print(msg_client) 
             #Enviar codigo
            
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
                        
            except ConnectionResetError as e:
                print(f"Erro de conexão: {e}")
                connection.send("555".encode('utf-8'))        
        
    def matchClients(self, chat):
        minNote = self.MinNote[chat.intensidade]
        
        while len(self.arvore) == 0:
            time.sleep(0.2)
            
        minNote = InfoCounselor(None, None, minNote)
        
        counselor = self.arvore.GetEqualOrMajor(minNote)
        with self.Lock:
            print(self.arvore.deleteNode(counselor).nickname)
        chat.addOnChat(counselor.nickname, counselor.socket)
        self.usersHashTable.get(counselor.nickname).chat = chat
        clients_socktes = chat.getClients()
        for connection in clients_socktes:
            connection.send(f"270&{chat.assunto}&{chat.intensidade}".encode('utf-8'))        
        return
        # while len(self.AllChats) != 0:
        #     for chat in self.AllChats.values():
        #         if chat.status == "active": continue
                
        #         while len(self.arvore) == 0:
        #             time.sleep(0.2)
                
        #         self.arvore.GetAndMajorOccurrences()
                
        #         chat.addOnChat(self.arvore[0][0], self.arvore[0][1]) # fazer a busca na arvore de um um conselheiro 
        #         chat_clients = chat.getClients()
        #         chat.changeStatus()
        #         self.usersHashTable.get(self.arvore[0][0]).chat = chat
                
                
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
