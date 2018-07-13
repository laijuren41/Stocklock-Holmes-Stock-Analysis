import requests

def get_stocks():
	url = 'http://localhost:8000/home/api/chart/data'

	r = requests.get(url)
	stocks = r.json()

	stock_arg = {'stocks':stocks}

	return stock_arg
