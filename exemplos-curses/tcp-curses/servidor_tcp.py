import socket
import multiprocessing
from threading import Thread

class Servidor_TCP:
	def __init__(self):
		self.HOST = '0.0.0.0'	# Endereco IP do Servidor
		self.PORT = 8000		# porta que o Servidor escuta
		self.TAM_MSG = 1024		# Tamanho máximo das mensagens 
		self.clientes = {}
		self.lock = multiprocessing.Lock()

	def processa_cliente(self, con, cliente):
		self.clientes[cliente] = con
		print(f'Cliente {cliente[0]}:{cliente[1]} conectado')
		while True:
			msg = con.recv(self.TAM_MSG)
			if not msg: break
			for c in self.clientes.values():
				c.send(msg)
		self.lock.acquire()
		try:
			self.clientes.pop(cliente)
		finally:
			self.lock.release()
		con.close()
		print(f'Cliente {cliente[0]}:{cliente[1]} desconectado')

	def start(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
		serv = (self.HOST, self.PORT)
		sock.bind(serv)
		sock.listen(50)
		while True:
			try:
				con, cliente = sock.accept()
			except: break
			Thread(target=self.processa_cliente, args=(con, cliente)).start()
		# Encerra conexões de clientes
		self.lock.acquire()
		try:
			for c in self.clientes.values():
				c.shutdown(socket.SHUT_RDWR)
				c.close()
		finally:
			self.lock.release()
		sock.close()
	
