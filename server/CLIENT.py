import socket, datetime, pickle, time, math
import multiprocessing as mp
import colorlabels as cl
from ARBITRUM_ENGINE import ArbitrumEngine


servers = {
	'38.242.230.255': 61252,  #
	'86.48.1.238': 61252,  #
	'86.48.1.239': 61252,  #
	'161.97.96.253': 61252,  #
	'161.97.96.242': 61252,  #
	'161.97.96.196': 61252,  #
	'161.97.96.205': 61252,  #
	'161.97.96.239': 61252,  #
	'173.249.12.156': 61252,  #
	'173.249.24.173': 61252,  #
	'173.249.28.128': 61252,  #
	'173.249.55.157': 61252,  #
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
		while True:
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
			
			self.procs = []
			
			ArbitrumEngine.calculate()

	
def client(ip: str, port: int, links: dict):
	sock = socket.socket()
	
	sock.connect((ip, port))
	print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.RED}СОЕДИНЕНИЕ С {ip}:{port} УСТАНОВЛЕНО')
	
	sock.send(str(links).encode())
	print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.YELLOW}ТАРГЕТЫ ДЛЯ ПАРСИНГА ОТПРАВЛЕНЫ\n')

	while True:
		raw = ''
		while True:
			try:
				while len(raw) != 2064:
					raw += sock.recv(1032).decode()
					time.sleep(0.5)
				raw = raw.split('::')
				
				if raw[0].isdigit():
					size = int(raw[0])
					name = raw[1]
					raw_data = raw[2].rstrip('0')
					break
			except Exception:
				print('--------------------\n\n', raw, '\n\n--------------------')
		
		raw = ''
		left = size - 2064
		if left <= 0:
			left = 0
		
		time.sleep(2)
		
		while left != 0:
			if left > 2064:
				left -= 2064
				while len(raw) != 2064:
					raw += sock.recv(1032).decode()
					time.sleep(0.5)
				raw_data += raw
				raw = ''
			else:
				while len(raw) != 2064:
					raw += sock.recv(1032).decode()
					time.sleep(0.5)
				raw_data += raw
				raw = ''
				left = 0
		
		data = eval(raw_data.replace(r'\u273a', '').replace('\u273a', '').rstrip('0'))
		with open(f'ExchangesData/{name.replace("|", "")}', 'w+') as file:
			file.write(str(data))
			print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.BRIGHT_GREEN}КОТИРОВКИ {name} СОХРАНЕНЫ\n\n')
		
		response = sock.recv(4).decode()
		if response == 'next': continue
		if response == 'end!': break
	
	sock.close()
	print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.RED}СОЕДИНЕНИЕ С {ip} ЗАКРЫТО')
	
	
if __name__ == '__main__':
	PClient().worker()
