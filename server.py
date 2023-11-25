import socket

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", port))
    server.listen(1)#socket do servidor especifica o número máximo de conexões pendentes que podem ser enfileiradas enquanto o servidor está lidando com uma conexão existente.
    
    print("Bem Vindo ao Chat!")
    print(f"Servidor aguardando conexao na porta {port}")

    connection, end_client = server.accept()
    print(f"Conexão estabelecida com {end_client}")

    while True:
        msg_client = connection.recv(1024).decode("utf-8")
        if not msg_client:
            break
        print(f"Cliente: {msg_client}")
        
        response = input("Servidor: ")
        connection.send(response.encode('utf-8'))

    connection.close()
    server.close()


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


if __name__ == "__main__":
    port = 12345
    start_server(port)
