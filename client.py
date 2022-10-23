import socket, pickle

servers = {
	'38.242.230.255': 35000,
	'86.48.1.238': 35001,
	'86.48.1.239': 35002,
	'161.97.96.253': 35003,
	'161.97.96.242': 35004,
	'161.97.96.196': 35005,
	'161.97.96.205': 35006,
	'161.97.96.239': 35007,
	'173.249.12.156': 35008,
	'173.249.24.173': 35009,
	'173.249.28.128': 35010,
	'173.249.55.157': 35011,
	'173.249.55.159': 35012
}


# for ip, port in servers:
# 	exec(f'''''')

class PClient:
	@staticmethod
	def client(ip: str, port: int, links: set):
		sock = socket.socket()
		
		sock.connect((ip, port))
		
		sock.send(str(links).encode())
		
		raw_data = sock.recv(10240).decode().split(' ')
		
		while raw_data:
			with open(f'ExchangesData/{raw_data[0]}', 'w+') as file:
				file.write(raw_data[1])
			
			raw_data = sock.recv(10240).decode().split(' ')
		
		sock.close()
		
		
		
