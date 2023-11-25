import socket

def start_client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", port))

    print("1 - login\n2 - signup")
    

    loginChoice = int(input("Escolha: "))
    if loginChoice == 1:
        login()
    if loginChoice == 2:
        sign()
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
    pass

def sign():
    pass
    
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
