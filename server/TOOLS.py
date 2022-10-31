import json
from threading import Lock


class tools:
	@staticmethod
	def filtration(date: str, filters) -> json:
		lock = Lock()
		
		lock.acquire()
		with open(f'ArbitrumData/{date}.json', 'r') as file:
			data = json.load(file)
		lock.release()
		
		Filtered_data = []
		for _ in data['currencies']:
			if not filters or 'g413gg' in filters:
				Filtered_data.append(_)

			if _['exchanges'][0]['name'] in filters or _['exchanges'][1]['name'] in filters:
				Filtered_data.append(_)
		
		data['currencies'] = Filtered_data
		
		return json.dumps(data)
		
		
	
	
	@staticmethod
	def sorting(data: list) -> list:
		return sorted(data, key=lambda k: float(k['spread'].replace('%', '')), reverse=True)
		
		