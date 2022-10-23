import socket, datetime, pickle, time, math

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


def NowTime():
	return f'{datetime.datetime.day}.' \
		   f'{datetime.datetime.month}.' \
		   f'{datetime.datetime.year} ' \
		   f'{datetime.datetime.hour}:' \
		   f'{datetime.datetime.minute}:' \
		   f'{datetime.datetime.second}'


class PClient:
	def __init__(self):
		with open('exchanges', 'rb') as file:
			self.raw_links = [[ex, link] for ex, link in pickle.load(file).items()]
		
		self.size = len(self.raw_links)
		
		self.const = math.ceil(self.size / len(servers))  # 13
	
	def worker(self):
		count = 0
		for ip, port in servers.items():
			links = {ex: link for ex, link in
					 self.raw_links[0 + ((self.const * count) % self.size): (self.const * (count + 1)) if (
							 ((self.const * (count + 1)) + bool(count)) < self.size) else self.size]}
			self.client(ip, port, links)
			count += 1
	
	@staticmethod
	def client(ip: str, port: int, links: dict):
		sock = socket.socket()
		
		sock.connect((ip, port))
		print(f'{NowTime()} СОЕДИНЕНИЕ С {ip}:{port} УСТАНОВЛЕНО')
		
		sock.send(str(links).encode())
		print(f'{NowTime()} ТАРГЕТЫ ДЛЯ ПАРСИНГА ОТПРАВЛЕНЫ\n')
		
		raw_data = sock.recv(10240).decode().split(' ')
		print(f'{NowTime()} ПОЛУЧЕНЫ КОТИРОВКИ {raw_data[0]}')
		
		while raw_data:
			with open(f'ExchangesData/{raw_data[0]}', 'w+') as file:
				file.write(raw_data[1])
				print(f'{NowTime()} КОТИРОВКИ {raw_data[0]} СОХРАНЕНЫ\n\n')
			
			raw_data = sock.recv(10240).decode().split(' ')
			print(f'{NowTime()} ПОЛУЧЕНЫ КОТИРОВКИ {raw_data[0]}')
		
		sock.close()
		print(f'{NowTime()} СОЕДИНЕНИЕ ЗАКРЫТО')


if __name__ == '__main__':
	PClient().worker()
