#! /usr/bin/env python3
import sys
from cliente_tcp import Cliente_TCP

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8000

    if len(sys.argv) > 1:
        HOST = sys.argv[1]

    cliente = Cliente_TCP(HOST, PORT)
    cliente.start()
