import socket

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
    
    loginChoice = int(input("Escolha: "))
    
    
    while True:
        if loginChoice == 1:
            log = login()
            client.send(log.encode("utf-8"))
            validate_login = client.recv(1024).decode("utf-8")
            print(f"Servidor: {validate_login}")

            if validate_login != "Usuário ou senha incorreto.":
                break


        elif loginChoice == 2:
            register = signup()
            client.send(register.encode("utf-8"))
            validate_register = client.recv(1024).decode("utf-8")
            print(f"Servidor: {validate_register}")

            if validate_register != "erro":
                break
        else:
            print("Não foi possivel Logar, tente novamente")
            return #remover esse break e tratar depois


    while True:
        menu()
        msg = input("Client: ")
        client.send(msg.encode("utf-8"))

        response_server = client.recv(1024).decode("utf-8")
        print(f"Servidor: {response_server}")

        if msg.upper() == "EXIT":
            break
        
    client.close()


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
