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
    
    
    while True:
        if loginChoice == "1":
            log = login()
            client.send(log.encode("utf-8"))
            validate_login = client.recv(1024).decode("utf-8")
            if validate_login == "200":
                print(translate[validate_login])
                break
            print(f"Servidor: {validate_login}")

        elif loginChoice == "2":
            register = signup()
            client.send(register.encode("utf-8"))
            validate_register = client.recv(1024).decode("utf-8")
            if validate_register == "210":
                print(translate[validate_register])
                break
           
        else:
            print("Não foi possivel Logar, tente novamente")
            return #remover esse break e tratar depois


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
        if response_server[0] == "CONECTED":
            print(response_server[1])
            threading.Thread(target=escutar, args=(client,)).start()
            break
        
    while True:
        msg = input(">> ")
        client.send(f"msg&{msg}".encode("utf-8"))
        
    response_server = client.recv(1024).decode("utf-8")
    print(f"Servidor: {response_server}")
    
    client.close()

def escutar(client):
    while True:
        try:
            response_server = client.recv(4096).decode("utf-8").split("&")
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

def signup():
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
