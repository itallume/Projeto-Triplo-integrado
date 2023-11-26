import socket
lista_usuarios = {
    
    "fernando": "123"
}
def start_server(port):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(1)#socket do servidor especifica o número máximo de conexões pendentes que podem ser enfileiradas enquanto o servidor está lidando com uma conexão existente.
    
    print("Bem Vindo ao Chat!")
    print(f"Servidor aguardando conexao na porta {port}")

    connection, end_client = server.accept()
    print(f"Conexão estabelecida com {end_client}")

    while True:
        msg_client = connection.recv(1024).decode("utf-8").split(" ")
        
        if msg_client[0] == "login":                                                                          
            if msg_client[1] in lista_usuarios:
                if lista_usuarios[msg_client[1]] ==  msg_client[2]:
                    connection.send("Login efetuado!".encode('utf-8'))
                    continue
                else:
                    connection.send("Usuário ou senha incorreto.".encode('utf-8'))
                    continue
            else:
                connection.send("Usuário ou senha incorreto.".encode('utf-8'))
                continue
        if msg_client[0] == "register":                                                                          
            if msg_client[1] in lista_usuarios:
                connection.send("erro".encode('utf-8'))
                continue
            lista_usuarios[msg_client[1]] = msg_client[2]
            connection.send("ok".encode('utf-8'))
            print(lista_usuarios)
            continue
               
                    
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
