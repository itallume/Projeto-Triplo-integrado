import socket
import threading 
import socket
from threading import Thread
import sys


translate = {
    "210": "Cadastro efetuado",
    "211": "Nome de usuário já existente",
    "200": "login efetuado", 
    "201": "Usuário ou senha incorreto",
    "220": "Tipo setado",
    "221": "Tipo inexistente",
    "230": "Tema definido",
    "231": "Intensidade inexistente", 
    "240": "Comunicação feita",
    "250": "Desconectado",
    "260": "Nota apurada",
    "261": "Nota inválida",
    "299": "Muitas tentativas de login, tente mais tarde.",
    "270": "Conectado a um chat",
    "555": "Erro no servidor"
}

def start_client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", port))
    print(f"Conectado ao servidor na porta {port}")

    def waitingConnection():    
        while True:
            response_server = client.recv(4096).decode("utf-8").split("&")
            print(response_server)
            if translate[response_server[0]] == "270":
                print(translate[response_server[0]], f"Assunto: {response_server[1]} Intensidade: {response_server[2]}")
            return
        
    def set_intensity(assunto):   
        while True:
            try:
                intensidade = int(input("Intensidade: "))
                assert intensidade in [1,2,3] # bug aqui PEDE MAIS DE UMA VEZ O MESMO INPUT CASO FOR ENVIADO INPUT INVALIDO<--------------------------------------
                break
            except Exception:
                print("\nEscolha uma intensidade válida (1, 2 ou 3)!\n")

        return client.send(f"type&undecided&{assunto}&{intensidade}".encode("utf-8"))


    def set_assunto():
        try:
            assunto = input()
            assert len(assunto) > 0
            if len(assunto) <= 3:
                return set_assunto()
        except Exception:
            print("Escreva um assunto Válido!")
            set_assunto()
            
        print("Escolha a intensidade:\n1: Baixa\n2: Média\n3: Alta")
        return set_intensity(assunto)

    def set_type():
        try:
            type = int(input("Escolha: "))
            if type not in [1,2]:
                return set_type()
        except Exception:
            print("\nTente novamente, escolha uma opção válida\n")
            return set_type()

        if type == 1:   
            print("Qual será o assunto? ")
            return set_assunto()

        if type == 2:
            print("\nEsperando por um(a) Indeciso(a)...\n")
            client.send(f"type&counselor".encode("utf-8"))
            return waitingConnection()
            

    def Validate_register():
        signup = signin()
        client.send(signup.encode("utf-8"))
        validate_signup = client.recv(4096).decode("utf-8")
        if validate_signup == "210":
            print("\n",translate[validate_signup]) #Cadastro efetuado com Sucesso!
        while validate_signup == "211": #while msm???
            print("\n",translate[validate_signup])
            print("Tente Novamente\n") #Nome de Usuario ja Existente, tente novamente!
            return Validate_register()
        
        print(f"Servidor: {validate_signup}")
        print("1. Indeciso(a)\n2. Conselheiro")
        return set_type()


    def Validate_login():
        log = login()
        client.send(log.encode("utf-8"))
        validate_login = client.recv(1024).decode("utf-8")
        if validate_login == "200":
            print("\n",translate[validate_login]) #Login efetuado com Sucesso!
        
        if validate_login == "299": # 
            print("\n",translate[validate_login])
            return Validate_login()

        while validate_login == "201":
            print("\n",translate[validate_login])
            print("Tente Novamente\n") #Login nao efetuado, Usuário ou Senha incorretos!
            return Validate_login()
        
        print(f"Servidor: {validate_login}")
        print("1. Indeciso(a)\n2. Conselheiro")
        return set_type()


    def validate_choice():
        try:
            loginChoice = int(input("Opção: "))
        except Exception:
            print("Não foi possivel Logar, tente novamente")
            return validate_choice()

        if loginChoice == 1:
            return Validate_login()
        elif loginChoice == 2:
            return Validate_register()
        
    conectado = True
    
    def escutar(): #cuidado com o login e signup eu achava  qmeu codg tava errado
        while True:
            response_server = client.recv(4096).decode("utf-8").split("&")
            if response_server[0] != "250":
                    print(response_server[1])
            else:
                global conectado
                conectado = False 
                break
            
    print("\n\n=============Bem-Vindo ao Conselheiro Virtual!=============\n")
    print("Escolha uma opção:")
    print("\n1 - login\n2 - signup\n")
    validate_choice()
    
    threading.Thread(target=escutar, args=()).start()       

    while conectado: # tira desse while para resolver bug do CLIENTE DESCONECTAR E ENVIAR MSG MSM ASSIM  
            msg = input(">> ")
            client.send(f"msg&{msg}".encode("utf-8"))
             
     #
             
def login():
    user = input("\nUsuario: ")
    password = input("Senha: ")
    response = f"login {user} {password}"
    return response

def signin():
    try:
        user = input("\nUsuario: ")
        password = input("Senha: ")
        assert len(password) >= 6
        assert len(user) >= 3 and len(user) <= 13
    except Exception:
        print("\nA senha deve conter 6 ou mais caracteres e o Usuario deve conter 3 ou mais caracteres!\n")
        return signin()
    response = f"register {user} {password}"
    return response
    
def menu():
    return('''
        Menu:
        1 - Receber conselhos (aconselhado)
        2 - Enviar conselhos (conselheiro)
        3 - Ver conselhos anteriores
        ''')

def subject():
    pass

def rate_user():
    pass

    





    
if __name__ == "__main__":
    port = 12345
    start_client(port)
