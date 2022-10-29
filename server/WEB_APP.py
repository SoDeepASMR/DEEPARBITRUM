from flask import Flask, render_template, request
from TOOLS import tools

app = Flask('DeepARBITRUM')


@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')


@app.route('/query-example')
def query_example():
	date = request.args.get('date').replace(':', '.')
	filters = request.args.get('filter')
	
	return tools.filtration(date, filters)
	
	
if __name__ == '__main__':
	app.run(debug=True)
