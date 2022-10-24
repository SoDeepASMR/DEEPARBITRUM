import socket, os, datetime, time
from ex_parser import parser


def NowTime():
	return f'{datetime.datetime.now().day}.' \
		   f'{datetime.datetime.now().month}.' \
		   f'{datetime.datetime.now().year} ' \
		   f'{datetime.datetime.now().hour}:' \
		   f'{datetime.datetime.now().minute}:' \
		   f'{datetime.datetime.now().second}'


if __name__ == '__main__':
	if not os.path.isdir('ExchangesData'):
		os.mkdir('ExchangesData')
		
	sock = socket.socket()
	
	sock.bind(('', 35000))
	
	while True:
		sock.listen(1)
		
		print(f'{NowTime()} ОЖИДАНИЕ ПОДКЛЮЧЕНИЯ')
		conn, addr = sock.accept()
		print(f'{NowTime()} СОЕДИНЕНИЕ С {addr} УСТАНОВЛЕНО')
		
		data = {}
		raw = None
		while not raw:
			raw = conn.recv(32768)
		exec(f'''data = {raw.decode()}''')
		print(data)
		print(f'{NowTime()} ПОЛУЧЕНА DATA')
		
		scan = parser(data)
		scan.worker()
		
		objects = []
		for (dirpath, dirnames, filenames) in os.walk('ExchangesData'):
			objects.extend(filenames)
		
		response = None
		for obj in objects:
			with open(f'ExchangesData/{obj}', 'r', encoding='utf-8') as file:
				packet = (obj + '::' + file.read().strip('\n')).encode()
				size = len(packet)
				left = size
				
				count = 0  # [0 + ((2000 * count) % size): (2000 * (count + 1)) if (((2000 * (count + 1)) + bool(count)) < size) else size]
				if size > 2900:
					while True:
						conn.send(packet[0 + ((2900 * count) % size): (2900 * (count + 1)) if (((2900 * (count + 1)) + bool(count)) < size) else size])
						count += 1
						left -= 2900
						
						while response != 'next':
							response = conn.recv(128).decode()
						response = None
						
						if left <= 0:
							conn.send('over'.encode())
							break
				else:
					conn.send(packet)
					
					while response != 'next':
						response = conn.recv(128).decode()
					response = None
					
					conn.send('over'.encode())
				
				print(f'{NowTime()} ОТПРАВЛЕНЫ КОТИРОВКИ {obj}')
				
				while response != 'next':
					response = conn.recv(128).decode()
				response = None
		
		conn.send('end'.encode())
		conn.close()
		print(f'\n{NowTime()} СОЕДИНЕНИЕ ЗАКРЫТО\n\n')
			
