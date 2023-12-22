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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
        self.sock.connect((self.host, self.port))
        print(f"Conectado ao servidor na porta {self.port}")
        print("\n\n=============Bem-Vindo ao Conselheiro Virtual!=============\n")
        print("Escolha uma opção:")
        print("\n1 - login\n2 - signup\n")
        self.validate_choice()

    def validate_choice(self):
        try:
            loginChoice = int(input("Opção: "))
        except Exception:
            print("Não foi possivel Logar, tente novamente")
            return self.validate_choice()

        if loginChoice == 1:
            self.Validate_login()
        elif loginChoice == 2:
            self.Validate_register()

    def Validate_login(self):
        log = self.login()
        self.sock.send(log.encode("utf-8"))
        validate_login = self.sock.recv(1024).decode("utf-8").split(" ")
        if validate_login[0] == "200": #translate bug 
            print(validate_login) #Login efetuado com Sucesso!
        
        if validate_login[0] == "299": #<---------#ranslate bug 
            print(validate_login)
            self.Validate_login()

        while validate_login[0] == "201":
            print(validate_login) #translate bug 
            print("Tente Novamente\n") #Login nao efetuado, Usuário ou Senha incorretos!
            self.Validate_login()
        
        print(f"Servidor: {validate_login}")
        print("1. Indeciso(a)\n2. Conselheiro")
        self.set_type()

    def Validate_register(self):
        signup = self.signin()
        self.sock.send(signup.encode("utf-8"))
        validate_signup = self.sock.recv(4096).decode("utf-8").split(" ")
        if validate_signup[0] == "210":
            print("\n",self.CodesTranslate[validate_signup[0]]) #Cadastro efetuado com Sucesso!
            
        while validate_signup[0] == "211": #while msm???
            print("\n",self.CodesTranslate[validate_signup[0]])
            print("Tente Novamente\n") #Nome de Usuario ja Existente, tente novamente!
            self.Validate_register()
        
        print(f"Servidor: {validate_signup}")
        print("1. Indeciso(a)\n2. Conselheiro(a)")
        self.set_type(validate_signup)

    def set_type(self, validate_signup):
        try:
            type = int(input("Escolha: "))
            if type not in [1,2]:
                self.set_type(validate_signup)
        except Exception:
            print("\nTente novamente, escolha uma opção válida\n")
            self.set_type(validate_signup)

        if type == 1:   
            print("Qual será o assunto? ")
            self.set_assunto()

        if type == 2:
            print("\nEsperando por um(a) Indeciso(a)...\n")
            self.sock.send(f"type&counselor".encode("utf-8"))
            response_server = self.sock.recv(4096).decode("utf-8").split("&")
            self.waitingConnection(response_server)

    def set_assunto(self):
        try:
            assunto = input()
            assert len(assunto) > 0
            if len(assunto) <= 3:
                self.set_assunto()
        except Exception:
            print("Escreva um assunto Válido!")
            self.set_assunto()
            
        print("Escolha a intensidade:\n1: Baixa\n2: Média\n3: Alta")
        self.set_intensity(assunto)

    def set_intensity(self, assunto):   
        while True:
            try:
                intensidade = int(input("Intensidade: "))
                
                 # bug aqui PEDE MAIS DE UMA VEZ O MESMO INPUT CASO FOR ENVIADO INPUT INVALIDO<--------------------------------------
                self.sock.send(f"type&undecided&{assunto}&{intensidade}".encode("utf-8"))
                response_server = self.sock.recv(4096).decode("utf-8").split("&")
                print("linha 132", response_server)
                if response_server[0] == "231":
                    print(self.CodesTranslate[response_server[0]])
                    self.set_intensity(assunto, self.sock)
                else:
                    print("aqui")
                    self.waitingConnection(response_server)
            except Exception:
                print("\nEscolha uma intensidade válida (1, 2 ou 3)!\n")

    def waitingConnection(self, response_server):   

        if response_server[0] == "270":
            print(response_server[0], f"Assunto: {response_server[1]} Intensidade: {response_server[2]}")
            self.conected = True
            print("Chat iniciado!")
            threading.Thread(target=self.escutar, args=()).start()
            self.DigitOnchat()
            
    def escutar(self):
        while True:
            response_server = self.sock.recv(4096).decode("utf-8").split("&")
            if response_server[0] != "250":
                print(response_server[1])
            else:
                print("VOCE FOI DESCONECTADO!!!")
                self.conected = False 
                break
            
    def DigitOnchat(self):
        while self.conected: # tira desse while para resolver bug do ServerSocketE DESCONECTAR E ENVIAR MSG MSM ASSIM  
                msg = input(">> ")
                self.sock.send(f"msg&{msg}".encode("utf-8"))

    def login(self): 
        while True:
            try:
                user = input("\nUsuario: ")
                password = input("Senha: ")
                response = f"login {user} {password}"
                return response
            except Exception:
                
                break

        

    def signin(self):
        try:
            user = input("\nUsuario: ")
            password = input("Senha: ")
            assert len(password) >= 6
            assert len(user) > 0 and len(user) <= 20
        except Exception:
            print("\nA senha deve conter 6 ou mais caracteres e o Usuario deve conter 1 ou mais caracteres!\n")
            return self.signin()
        response = f"register {user} {password}"
        return response


client = Client("localhost", 12345)
client.setDict() #atribuir valores do dicionário
client.start_client()
