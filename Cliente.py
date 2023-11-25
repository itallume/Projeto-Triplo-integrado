import socket

def start_client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", port))

    while True:
        msg = input("Client: ")
        client.send(msg.encode("utf-8"))

        response_server = client.recv(1024).decode("utf-8")
        print(f"Servidor: {response_server}")

        if msg.upper() == "EXIT":
            break
        
    client.close()


if __name__ == "__main__":
    port = 12345
    start_client(port)
