#! /usr/bin/env python3
from servidor_tcp import Servidor_TCP

if __name__ == "__main__":
    serv = Servidor_TCP()
    serv.start()
