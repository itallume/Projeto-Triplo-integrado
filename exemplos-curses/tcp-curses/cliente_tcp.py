import socket
import curses
import multiprocessing
from threading import Thread

class Cliente_TCP:
    def __init__(self, host_serv, port_serv):
        self.serv = (host_serv, port_serv)
        self.TAM_MSG = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = multiprocessing.Lock()

    def msg_receive(self):
        lasty, lastx = self.stdscr.getmaxyx() 
        msg_box = curses.newwin(lasty-2,lastx,0,0)
        msg_box.scrollok(True)
        while True:
            msg = self.sock.recv(self.TAM_MSG)
            if not msg: 
                # Thread main solicitou encerramento
                break
            self.lock.acquire()
            try:
                msg_box.addstr(f'Recebido> {msg.decode()}\n')
                msg_box.refresh()
                self.input_box.refresh()
            finally:
                self.lock.release()

    def input(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.echo()
        lasty, lastx = self.stdscr.getmaxyx() 
        self.input_box = curses.newwin(2,lastx,lasty-2,0)    
        Thread(target=self.msg_receive).start()
        while True:
            self.lock.acquire()
            try:
                self.input_box.clear()
                self.input_box.addstr('Enviar> ')
                self.input_box.refresh()
            finally:
                self.lock.release()
            try:
                msg = self.input_box.getstr().decode()
                if msg.lower() == 'sair':
                    try:
                        # Solicita fechamento do socket
                        self.sock.shutdown(socket.SHUT_RDWR)
                        self.sock.close()
                    except: pass
                    break
                self.sock.send(msg.encode())
            except: pass

    def start(self):
        self.sock.connect(self.serv)

        curses.wrapper(self.input)
