import json, os, datetime, time
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
	
	dates = [k.replace('.json', '').replace(' ', '.').split('.') for k in [_ for i, j, _ in os.walk('ArbitrumData')][0]]
	for _ in dates:
		_.append(time.mktime(datetime.date(int(_[2]), int(_[1]), int(_[0])).timetuple()) + int(_[3]) * 3600 + int(_[4]) * 60)
	
	dates = sorted(dates, key=lambda k: k[5], reverse=True)[0]
	
	lock.acquire()
	last_date = f'{dates[0]}.{dates[1]}.{dates[2]} {dates[3]}.{dates[4]}'
	
	action = request.args.get('action')
	date = request.args.get('date').replace(':', '.')
	filters = request.args.get('filter')
	
	if 'g413gg' in date and 'g413gg' in filters:
		with open(f'ArbitrumData/{last_date}.json', 'r') as file:
			j = json.load(file)
		lock.release()
		
		return j
	
	if action == 'update': return tools.filtration(last_date, filters)
	
	else: return tools.filtration(date, filters)
	
	
if __name__ == '__main__':
	app.run(debug=False)
