import socket, os, datetime, time
from EXCHANGE_PARSER import parser
import colorlabels as cl


def sizing5(text: str) -> str:
	while len(text) < 5:
		text = '0' + text
	
	return text


def sizing2064(text: str) -> str:
	if len(text) < 2064:
		text += '0' * (2064 - len(text))
	
	return text


def NowTime() -> str:
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
	
	sock.bind(('', 61252))
	
	def main():
		try:
			while True:
				sock.listen(1)
				
				print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.YELLOW}ОЖИДАНИЕ ПОДКЛЮЧЕНИЯ')
				conn, addr = sock.accept()
				# while True:
				# 	conn, addr = sock.accept()
				# 	if '185.182.185.203' in addr: break
				# 	conn.close()
				print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.RED}СОЕДИНЕНИЕ С {addr} УСТАНОВЛЕНО')
				
				raw = None
				while not raw:
					raw = conn.recv(2064)
				data = eval(raw.decode())
				print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.BRIGHT_MAGENTA}ПОЛУЧЕНА DATA')
				
				scan = parser(data)
				scan.worker()
				
				objects = []
				for (_, _, filenames) in os.walk('ExchangesData'):
					objects.extend(filenames)
					
				for obj in objects:
					with open(f'ExchangesData/{obj}', 'r') as file:
						packet = '::' + obj + '::' + file.read().strip('\n')
						intsize = len(packet) + 5
						size = sizing5(str(intsize))
						packet = size + packet
						
						left = intsize
						count = 0
						if intsize > 2064:
							while True:
								if left == 0: break
								
								minipacket = packet[0 + ((2064 * count) % intsize): (2064 * (count + 1)) if (((2064 * (count + 1)) + bool(count)) < intsize) else intsize]
								
								if len(minipacket) < 2064:
									conn.send(sizing2064(minipacket).encode())
									left = 0
									
								else:
									conn.send(minipacket.encode())
									count += 1
									left -= 2064
						
						else:
							conn.send(sizing2064(packet).encode())
						
						print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.GREEN}ОТПРАВЛЕНЫ КОТИРОВКИ {obj}')
					
					if objects.index(obj) == len(objects) - 1: conn.send('end!'.encode())
					else: conn.send('next'.encode())
				
				conn.close()
				print(f'{cl.BRIGHT_WHITE}{NowTime()} {cl.RED}СОЕДИНЕНИЕ {addr} ЗАКРЫТО\n\n')
				time.sleep(10)
				
		except Exception: main()

	main()
