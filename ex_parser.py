import time, pickle, os
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
import multiprocessing as mp


class parser:
	def __init__(self, links):
		self.links = links
		
		self.parser = ExchangeParser()
	
	def worker(self):
		self.procs = []
		for ex, link in self.links.items():
			proc = mp.Process(target=self.parser.parse(), args=(ex, link,))
			self.procs.append(proc)
			proc.start()
			time.sleep(0.3)
		
		for proc in self.procs:
			proc.join()
	
	@staticmethod
	def get_exchanges():
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
		
		driver.get('https://coinmarketcap.com/en/rankings/exchanges/')
		
		driver.execute_script('window.scrollTo(0, 5000)')
		
		time.sleep(1)
		
		driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div[3]').click()
		
		time.sleep(1)
		
		links = [[_.text, _.get_attribute('href')] for _ in driver.find_elements(By.TAG_NAME, 'a')[1:171] if
				 _.get_attribute('href') is not None and 'https://coinmarketcap.com/exchanges/' in _.get_attribute(
					 'href')]
		links = [[ex, link[0:25] + '/en' + link[25:] + '?type=spot'] for [ex, link] in links]
		links = {ex: link for ex, link in links}
		
		links.update({'Uniswap (V3)': 'https://coinmarketcap.com/en/exchanges/uniswap-v3/?type=spot',
					  'Curve Finance': 'https://coinmarketcap.com/en/exchanges/curve-finance/?type=spot',
					  'Uniswap (V2)': 'https://coinmarketcap.com/en/exchanges/uniswap-v2/?type=spot',
					  'DODO (Ethereum)': 'https://coinmarketcap.com/en/exchanges/dodo/?type=spot',
					  'PancakeSwap (V2)': 'https://coinmarketcap.com/en/exchanges/pancakeswap-v2/?type=spot',
					  'iZiSwap': 'https://coinmarketcap.com/en/exchanges/iziswap/?type=spot',
					  'KLAYswap': 'https://coinmarketcap.com/en/exchanges/klayswap/?type=spot',
					  'SushiSwap': 'https://coinmarketcap.com/en/exchanges/sushiswap/?type=spot',
					  'Sun.io': 'https://coinmarketcap.com/en/exchanges/justswap/?type=spot',
					  'Uniswap (V3-Polygon)': 'https://coinmarketcap.com/en/exchanges/uniswap-v3-polygon/?type=spot'})
		
		driver.close()
		
		with open('exchanges', 'wb+') as file:
			pickle.dump(links, file)


class ExchangeParser:
	def __init__(self):
		# self.data = {'Pair': {'Price': None, 'Volume': None, 'Liq': None}}
		self.data = []
	
	def parse(self, exchange: str, link: str):
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('--ignore-certificate-errors-spki-list')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome('chromedriver.exe', chrome_options=options, service_log_path=None)
		
		print(exchange + '\n')
		
		while not self.data:
			driver.get(link)
			
			self.data = [_.text.split('\n') for _ in driver.find_elements(By.TAG_NAME, 'tr')[1:]]
			
		driver.close()
		
		self.data = [[_[2], _[3], _[6], _[7]] for _ in self.data]
		self.data = {Pair: {'Price': Price, 'Volume': Volume, 'Liq': Liq} for Pair, Price, Volume, Liq in self.data}
		
		with open(f'ExchangesData/{exchange}', 'w+') as file:
			file.write(str(self.data))
			print(exchange + ' DONE!')
			del self.data, options, driver

#
# if __name__ == '__main__':
# 	if not os.path.isdir('ExchangesData'):
# 		os.mkdir('ExchangesData')
# 	parser().worker()
