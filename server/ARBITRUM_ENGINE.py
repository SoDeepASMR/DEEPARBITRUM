import os, json, datetime
from TOOLS import tools


def timing():
	date = datetime.datetime.now()
	
	return f'{date.day}.{date.month}.{date.year} {date.hour}.{date.minute}'


class ArbitrumEngine:
	@staticmethod
	def calculate():
		data = []
		exchanges = [_ for i, j, _ in os.walk('ExchangesData')][0]
		
		for f in exchanges:
			with open(f'ExchangesData/{f}', 'r') as exs:
				d = eval(exs.read())
				data.append(d)
		
		updateDate = timing()
		arbitrage = {
			"relevant": True,
			"updateDate": updateDate,
			"currencies": []
		}
		
		size = len(data)
		for i in range(size):
			for j in range(size):
				
				if i == j: continue
				
				for pair in data[i].keys():
					if pair in data[j].keys():
						if '*' in data[i][pair]['Price'] or '*' in data[j][pair]['Price']: continue
						
						a = float(data[i][pair]['Price'].replace('$', '').replace(',', '').replace('*', '').strip())
						b = float(data[j][pair]['Price'].replace('$', '').replace(',', '').replace('*', '').strip())
						
						if a > b and (a / b - 1) * 100 > 1.5:
							arbitrage["currencies"].append(
								{
									"currency": pair,
									"spread": round((a / b - 1) * 100, 3),
									"exchanges": [
										{
											"name": exchanges[i],
											"price": data[i][pair]['Price'],
											"volume": data[i][pair]['Volume'],
											"liquidity": data[i][pair]['Liq']
										},
										{
											"name": exchanges[j],
											"price": data[j][pair]['Price'],
											"volume": data[j][pair]['Volume'],
											"liquidity": data[j][pair]['Liq']
										}
									]
								}
							)
						
						elif a < b and (b / a - 1) * 100 > 1.5:
							arbitrage["currencies"].append(
								{
									"currency": pair,
									"spread": round((b / a - 1) * 100, 3),
									"exchanges": [
										{
											"name": exchanges[j],
											"price": data[j][pair]['Price'],
											"volume": data[j][pair]['Volume'],
											"liquidity": data[j][pair]['Liq']
										},
										{
											"name": exchanges[i],
											"price": data[i][pair]['Price'],
											"volume": data[i][pair]['Volume'],
											"liquidity": data[i][pair]['Liq']
										}
									]
								}
							)
		
		arbitrage['currencies'] = tools.sorting(arbitrage['currencies'])
		
		with open(f'ArbitrumData/{updateDate}.json', 'w+') as file:
			json.dump(arbitrage, file)

ArbitrumEngine.calculate()