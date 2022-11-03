import json
from threading import Lock


class tools:
	@staticmethod
	def filtration(date: str, filters: str) -> json:
		lock = Lock()

		lock.acquire()
		with open(f'ArbitrumData/{date}.json', 'r') as file:
			data = json.load(file)
		lock.release()

		filters = filters.lower().strip().replace('[', '').replace(']', '').split(',')

		if len(filters) > 1:
			Filtered_data = []
			for _ in data['currencies']:
				if _['exchanges'][0]['name'].lower() in filters and _['exchanges'][1]['name'].lower() in filters:
					Filtered_data.append(_)

		else:
			Filtered_data = []
			for _ in data['currencies']:
				if not filters or 'g413gg' in filters:
					Filtered_data.append(_)

				elif _['exchanges'][0]['name'].lower() in filters or _['exchanges'][1]['name'].lower() in filters:
					Filtered_data.append(_)
		
		data['currencies'] = Filtered_data
		
		return json.dumps(data)
		
		
	
	
	@staticmethod
	def sorting(data: list) -> list:
		return sorted(data, key=lambda k: float(k['spread'].replace('%', '')), reverse=True)
		
		