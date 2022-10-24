import socket, datetime, pickle, time, math
import multiprocessing as mp
import colorlabels as cl


servers = {
	'38.242.230.255': 35000,
	'86.48.1.238': 35000,
	'86.48.1.239': 35000,
	'161.97.96.253': 35000,
	'161.97.96.242': 35000,
	'161.97.96.196': 35000,
	'161.97.96.205': 35000,
	'161.97.96.239': 35000,
	'173.249.12.156': 35000,
	'173.249.24.173': 35000,
	'173.249.28.128': 35000,
	'173.249.55.157': 35000,
	'173.249.55.159': 35000
}


def NowTime():
	return f'{datetime.datetime.now().day}.' \
		   f'{datetime.datetime.now().month}.' \
		   f'{datetime.datetime.now().year} ' \
		   f'{datetime.datetime.now().hour}:' \
		   f'{datetime.datetime.now().minute}:' \
		   f'{datetime.datetime.now().second}'


class PClient:
	def __init__(self):
		with open('exchanges', 'rb') as file:
			self.raw_links = [[ex.replace('|', ''), link] for ex, link in pickle.load(file).items()]

		self.procs = []
		
		self.size = len(self.raw_links)
		
		self.const = math.ceil(self.size / len(servers))  # 13
	
	def worker(self):
		count = 0
		for ip, port in servers.items():
			links = {ex: link for ex, link in
					 self.raw_links[0 + ((self.const * count) % self.size): (self.const * (count + 1)) if (
							 ((self.const * (count + 1)) + bool(count)) < self.size) else self.size]}
			proc = mp.Process(target=client, args=(ip, port, links,))
			self.procs.append(proc)
			proc.start()
			count += 1
		
		for p in self.procs:
			p.join()

	
def client(ip: str, port: int, links: dict):
	sock = socket.socket()
	
	sock.connect((ip, port))
	print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.RED}СОЕДИНЕНИЕ С {ip}:{port} УСТАНОВЛЕНО')
	
	sock.send(str(links).encode())
	print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.YELLOW}ТАРГЕТЫ ДЛЯ ПАРСИНГА ОТПРАВЛЕНЫ\n')
	
	while True:
		raw = None
		raw_data = None
		while not raw:
			raw = sock.recv(2900)
			raw_data = raw
		
		if raw.decode() == 'end': break
		
		sock.send('next'.encode())
		raw = None
		while raw != 'over':
			while not raw:
				raw = sock.recv(2900)
			
			if raw.decode() == 'over': break
			
			raw_data += raw
			sock.send('next'.encode())
			raw = None
	
		raw_data = raw_data.decode().split('::')
		print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.GREEN}ПОЛУЧЕНЫ КОТИРОВКИ {raw_data[0]}')
		
		with open(f'ExchangesData/{raw_data[0].replace("|", "")}', 'w+') as file:
			file.write(raw_data[1].replace(r'\u273a', '').replace('\u273a', ''))
			print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.BRIGHT_GREEN}КОТИРОВКИ {raw_data[0]} СОХРАНЕНЫ\n\n')
		
		sock.send('next'.encode())
		
	sock.close()
	print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.RED}СОЕДИНЕНИЕ С {ip} ЗАКРЫТО')


if __name__ == '__main__':
	PClient().worker()
