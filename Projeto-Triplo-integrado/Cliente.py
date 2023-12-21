import socket
import threading 
import socket
import threading
import sys


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.CodesTranslate = None
        self.conected = False
        self.lock = threading.Lock()


    def setDict(self):

        self.CodesTranslate = {
        "200": "login efetuado",
        "201": "Usuário ou senha incorreto",
        "210": "Cadastro efetuado",
        "211": "Nome de usuário já existente",
        "220": "Tipo setado",
        "221": "Tipo inexistente",
        "230": "Tema definido",
        "231": "Intensidade inexistente", 
        "240": "Comunicação feita",
        "250": "Desconectado",
        "260": "Nota apurada",
        "261": "Nota inválida",
        "270": "Conectado a um chat",
        "299": "Muitas tentativas de login, tente mais tarde.",
        "555": "Erro no servidor"
    }

    def start_client(self):
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ServerSocket.connect((self.host, self.port))
        print(f"Conectado ao servidor na porta {self.port}")
        print("\n\n=============Bem-Vindo ao Conselheiro Virtual!=============\n")
        print("Escolha uma opção:")
        print("\n1 - login\n2 - signup\n")
        self.validate_choice(ServerSocket)

    def validate_choice(self, ServerSocket):
        try:
            loginChoice = int(input("Opção: "))
        except Exception:
            print("Não foi possivel Logar, tente novamente")
            return self.validate_choice(ServerSocket)

        if loginChoice == 1:
            self.Validate_login(ServerSocket)
        elif loginChoice == 2:
            self.Validate_register(ServerSocket)

    def Validate_login(self, ServerSocket):
        log = self.login()
        ServerSocket.send(log.encode("utf-8"))
        validate_login = ServerSocket.recv(1024).decode("utf-8").split(" ")
        if validate_login[0] == "200":
            print("\n",self.CodesTranslate[validate_login]) #Login efetuado com Sucesso!
        
        if validate_login[0] == "299": # 
            print("\n",self.CodesTranslate[validate_login])
            self.Validate_login(ServerSocket)

        while validate_login[0] == "201":
            print("\n",self.CodesTranslate[validate_login])
            print("Tente Novamente\n") #Login nao efetuado, Usuário ou Senha incorretos!
            self.Validate_login(ServerSocket)
        
        print(f"Servidor: {validate_login}")
        print("1. Indeciso(a)\n2. Conselheiro")
        self.set_type(ServerSocket)

    def Validate_register(self, ServerSocket):
        signup = self.signin()
        ServerSocket.send(signup.encode("utf-8"))
        validate_signup = ServerSocket.recv(4096).decode("utf-8").split(" ")
        if validate_signup == "210":
            print("\n",self.CodesTranslate[validate_signup]) #Cadastro efetuado com Sucesso!
            
        while validate_signup == "211": #while msm???
            print("\n",self.CodesTranslate[validate_signup])
            print("Tente Novamente\n") #Nome de Usuario ja Existente, tente novamente!
            self.Validate_register(ServerSocket)
        
        print(f"Servidor: {validate_signup}")
        print("1. Indeciso(a)\n2. Conselheiro(a)")
        self.set_type(ServerSocket)

    def set_type(self, ServerSocket):
        try:
            type = int(input("Escolha: "))
            if type not in [1,2]:
                self.set_type(ServerSocket)
        except Exception:
            print("\nTente novamente, escolha uma opção válida\n")
            self.set_type(ServerSocket)

        if type == 1:   
            print("Qual será o assunto? ")
            self.set_assunto(ServerSocket)

        if type == 2:
            print("\nEsperando por um(a) Indeciso(a)...\n")
            ServerSocket.send(f"type&counselor".encode("utf-8"))
            self.waitingConnection(ServerSocket)

    def set_assunto(self, ServerSocket):
        try:
            assunto = input()
            assert len(assunto) > 0
            if len(assunto) <= 3:
                self.set_assunto(ServerSocket)
        except Exception:
            print("Escreva um assunto Válido!")
            self.set_assunto(ServerSocket)
            
        print("Escolha a intensidade:\n1: Baixa\n2: Média\n3: Alta")
        self.set_intensity(assunto, ServerSocket)

    def set_intensity(self, assunto, ServerSocket):   
        while True:
            try:
                intensidade = int(input("Intensidade: "))
                assert intensidade in [1,2,3] # bug aqui PEDE MAIS DE UMA VEZ O MESMO INPUT CASO FOR ENVIADO INPUT INVALIDO<--------------------------------------
                ServerSocket.send(f"type&undecided&{assunto}&{intensidade}".encode("utf-8"))
                response_server = ServerSocket.recv(4096).decode("utf-8").split(" ")
                if response_server[0] == "231":
                    print(self.CodesTranslate[response_server[0]])
                    self.set_intensity(assunto, ServerSocket)
                else:
                    print("aqui")
                    self.waitingConnection(ServerSocket)
            except Exception:
                print("\nEscolha uma intensidade válida (1, 2 ou 3)!\n")

    def waitingConnection(self, ServerSocket):    
        while True:
            response_server = ServerSocket.recv(4096).decode("utf-8").split("&")
            print(response_server)
            if self.CodesTranslate[response_server[0]] == "270":
                print(self.CodesTranslate[response_server[0]], f"Assunto: {response_server[1]} Intensidade: {response_server[2]}")
            threading.Thread(target=self.escutar, args=(ServerSocket,)).start()
            self.DigitOnchat(ServerSocket)
            
    def escutar(self, ServerSocket):
        while True:
            response_server = ServerSocket.recv(4096).decode("utf-8").split("&")
            if response_server[0] != "250":
                print(response_server[1])
            else:
                
                self.conected = False 
                break
            
    def DigitOnchat(self, ServerSocket):
        while self.conected: # tira desse while para resolver bug do ServerSocketE DESCONECTAR E ENVIAR MSG MSM ASSIM  
                msg = input(">> ")
                ServerSocket.send(f"msg&{msg}".encode("utf-8"))

    def login(self):
        user = input("\nUsuario: ")
        password = input("Senha: ")
        response = f"login {user} {password}"
        return response

    def signin(self):
        try:
            user = input("\nUsuario: ")
            password = input("Senha: ")
            assert len(password) >= 6
            assert len(user) >= 3 and len(user) <= 13
        except Exception:
            print("\nA senha deve conter 6 ou mais caracteres e o Usuario deve conter 3 ou mais caracteres!\n")
            return self.signin()
        response = f"register {user} {password}"
        return response


client = Client("localhost", 12345)
client.setDict()
client.start_client()
