import socket
import threading 
translate = {
    "210": "cadastro efetuado",
    "211": "Nome de usuário já existente",
    "200": "login efetuado", 
    "201": "Usuário ou senha errado",
    "220": "Tipo setado",
    "221": "Tipo inexistente",
    "230": "Tema definido",
    "231": "Intensidade inexistente", 
    "240": "comunicação feita",
    "250": "Desconectado",
    "260": "nota apurada",
    "261": "Nota inválida",

}

def start_client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", port))
    print(f"Conectado ao servidor na porta {port}")


    def set_intensity(assunto):   
        try:
            intensidade = int(input("Qual a intensidade? "))
            assert intensidade in [1,2,3] and intensidade.isnumeric()
        except Exception:
            print("\nEscolha uma intensidade válida!\n")
            return set_intensity(assunto) #talvez ocasione em bug

        return client.send(f"type&undecided&{assunto}&{intensidade}".encode("utf-8"))


    def set_assunto():
        try:
            assunto = input()
            assert assunto.isalpha() and len(assunto) > 0
        except Exception:
            print("\nEscreva um assunto Válido!\n")
            set_assunto()
            
        print("Escolha a intensidade:\n1: Baixa\n2: Média\n3: Alta")
        return set_intensity(assunto)

    def set_type():
        try:
            type = int(input("Escolha: "))
        except Exception:
            print("\nTente novamente, escolha uma opção válida\n")
            return set_type()

        if type == 1:   
            print("Qual será o assunto? ")
            return set_assunto()

        if type == 2:
            print("\nEsperando por um(a) Indeciso(a)...\n")
            client.send(f"type&counselor".encode("utf-8"))


    def Validate_register():
        signup = signin()
        client.send(signup.encode("utf-8"))
        validate_signup = client.recv(1024).decode("utf-8")
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

    print("\n\n=============Bem-Vindo ao Conselheiro Virtual!=============\n")
    print("Escolha uma opção:")
    print("\n1 - login\n2 - signup\n")
    validate_choice()




        
        
    while True:
        response_server = client.recv(4096).decode("utf-8").split("&")
        print()
        print(response_server[1])
        print()
        threading.Thread(target=escutar, args=(client,)).start()
        break

    conectado = True
    while conectado: # tira desse while para resolver bug do CLIENTE DESCONECTAR E ENVIAR MSG MSM ASSIM  
            msg = input(">> ")
            client.send(f"msg&{msg}".encode("utf-8"))
        
    print("sai!")
    
    def escutar(client): #cuidado com o login e signup eu achava  qmeu codg tava errado
        while True:
            response_server = client.recv(4096).decode("utf-8").split("&")
            if response_server != 250:
                    print(response_server[1])
            else:
                global conectado
                conectado = False 
                break       
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
        assert len(user) >= 3 len(user) <= 13
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
