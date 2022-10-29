import json, os
from flask import Flask, render_template, request
from TOOLS import tools
from threading import Lock

app = Flask('DeepARBITRUM', template_folder='templates')


@app.route("/")
@app.route("/index")
def index():
	return render_template('tailwind.html')


@app.route('/get')
def query_example():
	lock = Lock()
	try:
		date = request.args.get('date').replace(':', '.')
		filters = request.args.get('filter')
		print('date  ', date)
		print('filters  ', filters)
	except Exception:
		dates = [k.replace('.json', '').replace(' ', '.').split('.') for k in [_ for i, j, _ in os.walk('ArbitrumData')][0]]
		dates = sorted(dates, key=lambda k: k[2], reverse=True)
		dates = sorted(dates, key=lambda k: k[1], reverse=True)
		dates = sorted(dates, key=lambda k: k[0], reverse=True)
		dates = sorted(dates, key=lambda k: k[3], reverse=True)
		dates = sorted(dates, key=lambda k: k[4], reverse=True)
		
		lock.acquire()
		last_date = f'{dates[0][0]}.{dates[0][1]}.{dates[0][2]} {dates[0][3]}.{dates[0][4]}.json'
		with open(f'ArbitrumData/{last_date}', 'r') as file:
			j = json.load(file)
		lock.acquire()
		
		return json.load(file)
	
	return tools.filtration(date, filters)
	
	
if __name__ == '__main__':
	app.run(debug=True)
