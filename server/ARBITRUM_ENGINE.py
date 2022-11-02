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
			with open(f'ExchangesData/{f}', 'r', encoding='utf-8') as exs:
				d = eval(exs.read())
				data.append(d)
		
		updateDate = timing()
		arbitrage = {
			"relevant": True,
			"updateDate": updateDate,
			"currencies": []
		}

		selected_pairs = []
		size = len(data)
		for i in range(size):
			for j in range(size):
				
				if i == j: continue
				
				for pair in data[i].keys():
					if pair in data[j].keys():
						if '*' in data[i][pair]['Price'] or '*' in data[j][pair]['Price']: continue
						
						a = float(data[i][pair]['Price'].replace('$', '').replace(',', '').replace('*', '').strip(' ').replace('<', ''))
						b = float(data[j][pair]['Price'].replace('$', '').replace(',', '').replace('*', '').strip(' ').replace('<', ''))
						
						if a > b and 15 > (a / b - 1) * 100 >= 1 and int(data[i][pair]['Liq']) > 100 and int(data[j][pair]['Liq']) > 100 and [pair, exchanges[i], exchanges[j]] not in selected_pairs:
							selected_pairs.append([pair, exchanges[i], exchanges[j]])
							arbitrage["currencies"].append(
								{
									"currency": pair,
									"spread": str(round((a / b - 1) * 100, 3)) + '%',
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
						
						elif a < b and 15 > (b / a - 1) * 100 >= 1 and int(data[i][pair]['Liq']) > 100 and int(data[j][pair]['Liq']) > 100 and pair not in selected_pairs:
							selected_pairs.append([pair, exchanges[j], exchanges[i]])
							arbitrage["currencies"].append(
								{
									"currency": pair,
									"spread": str(round((b / a - 1) * 100, 3)) + '%',
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
