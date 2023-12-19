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

    print("1 - login\n2 - signup")
    
    loginChoice = input("Escolha: ")
    
    def Validate_register():
        signup = signin()
        client.send(signup.encode("utf-8"))
        validate_signup = client.recv(1024).decode("utf-8")
        if validate_signup == "210":
            print(translate[validate_signup]) #Cadastro efetuado com Sucesso!
        while validate_signup == "211": #while msm???
            print(translate[validate_signup]) #Nome de Usuario ja Existente, tente novamente!
            return Validate_register()
        
        print(f"Servidor: {validate_signup}")
        return


    def Validate_login():
        log = login()
        client.send(log.encode("utf-8"))
        validate_login = client.recv(1024).decode("utf-8")
        if validate_login == "200":
            print(translate[validate_login]) #Login efetuado com Sucesso!

        while validate_login == "201":
            print(translate[validate_login]) #Login nao efetuado, Usuário ou Senha incorretos!
            return Validate_login()
        
        print(f"Servidor: {validate_login}")
        return

    while True:
        if loginChoice == "1":
            Validate_login()

        elif loginChoice == "2":
            Validate_register()

        else:
            print("Não foi possivel Logar, tente novamente")
        break #remover esse break e tratar depois


    while True:
        # fernando ou paulo, se puder transformar isso em metodo é mt bom
        type = input("Deseja ser:\n1. Indeciso(a)\n2. Conselheiro")
        if type == "1":
            assunto = input("Qual será o assunto? ")
            intensidade = input("Qual a intensidade? ")
            client.send(f"type&undecided&{assunto}&{intensidade}".encode("utf-8"))
            break
        if type == "2":
            client.send(f"type&counselor".encode("utf-8"))
            break
        
    while True:
        response_server = client.recv(1024).decode("utf-8").split("&")
        if response_server[1] != 'exit':
            print(response_server[1])
            threading.Thread(target=escutar, args=(client,)).start()
        break
        
    while True: # tira desse while para resolver bug do CLIENTE DESCONECTAR E ENVIAR MSG MSM ASSIM
        msg = input(">> ")
        client.send(f"msg&{msg}".encode("utf-8"))
        

def escutar(client):
    while True:
        try:
            response_server = client.recv(4096).decode("utf-8").split("&")
            print(response_server[1])
            assert response_server[0] != "250"
        except Exception:
            print("Desconectado")
            client.close()
            break
    
def login():
    user = input("usuario: ")
    password = input("senha: ")
    response = f"login {user} {password}"
    return response

def signin():
    user = input("usuario: ")
    password = input("senha: ")
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
