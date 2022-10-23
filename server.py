import socket, os
from ex_parser import parser

if __name__ == '__main__':
	if not os.path.isdir('ExchangesData'):
		os.mkdir('ExchangesData')
		
	sock = socket.socket()
	
	sock.bind(('', 35000))
	
	while True:
		sock.listen(1)
		
		conn, addr = sock.accept()
		
		data = {}
		exec(f'''data = {conn.recv(10240).decode()}''')
		
		scan = parser(data)
		scan.worker()
		
		objects = []
		for (dirpath, dirnames, filenames) in os.walk('ExchangesData'):
			objects.extend(filenames)
			
		for obj in objects:
			with open(f'ExchangesData/{file}', 'r', encoding='utf-8') as file:
				conn.send((obj + ' ' + file.read().strip('\n')).encode())
		
		conn.close()
			
