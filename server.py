import socket, os, datetime
from ex_parser import parser


def time():
	return f'{datetime.datetime.day}.{datetime.datetime.month}.{datetime.datetime.year} {datetime.datetime.hour}:{datetime.datetime.minute}:{datetime.datetime.second}'


if __name__ == '__main__':
	if not os.path.isdir('ExchangesData'):
		os.mkdir('ExchangesData')
		
	sock = socket.socket()
	
	sock.bind(('', 35000))
	
	while True:
		sock.listen(1)
		
		print(f'{time()} ОЖИДАНИЕ ПОДКЛЮЧЕНИЯ')
		conn, addr = sock.accept()
		print(f'{time} СОЕДИНЕНИЕ С {addr} УСТАНОВЛЕНО')
		
		data = {}
		exec(f'''data = {conn.recv(10240).decode()}''')
		print(f'{time()} ПОЛУЧЕНА DATA')
		
		scan = parser(data)
		scan.worker()
		
		objects = []
		for (dirpath, dirnames, filenames) in os.walk('ExchangesData'):
			objects.extend(filenames)
			
		for obj in objects:
			with open(f'ExchangesData/{file}', 'r', encoding='utf-8') as file:
				conn.send((obj + ' ' + file.read().strip('\n')).encode())
				print(f'{time()} ОТПРАВЛЕНЫ КОТИРОВКИ {obj}')
		
		conn.close()
		print(f'{time()} СОЕДИНЕНИЕ ЗАКРЫТО\n\n')
			
